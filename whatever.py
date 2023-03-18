'''
This is the starting point for your serverless API.
It can be named anything you want, but needs to have the following:

- import runpod
- start function

To return an error, return a dictionary with the key "error" and the value being the error message.
'''

import runpod  # Required
import base64
import http
import io
import time
from json import JSONDecodeError
from typing import Optional

import requests
from PIL import Image
from fastapi import Header, Depends, Form, File, Request, APIRouter, UploadFile
from fastapi.openapi.models import Response
from pydantic import ValidationError
from starlette.responses import JSONResponse

from carvekit.web.deps import config, ml_processor
from carvekit.web.handlers.response import handle_response, Authenticate
from carvekit.web.responses.api import error_dict
from carvekit.web.schemas.request import Parameters, VertexAIParameters
from carvekit.web.utils.net_utils import is_loopback
from carvekit.web.utils.init_utils import init_interface
from carvekit.web.schemas.config import WebAPIConfig
from carvekit.web.utils.init_utils import init_config
from carvekit.web.other.removebg import process_remove_bg


def is_even(job):
    payload = job["input"]
    bg = None
    # payload = None
    # try:
    #     payload = await parameters.json()
    # except JSONDecodeError:
    #     return JSONResponse(content=error_dict("Empty json"), status_code=400)
    try:
        parameters = Parameters(**payload)
    except ValidationError as e:
        return Response(
            content=e.json(), status_code=400, media_type="application/json"
        )
    if parameters.image_file_b64 is None and parameters.image_url is None:
        return JSONResponse(content=error_dict("File not found"), status_code=400)

    if parameters.image_file_b64:
        if len(parameters.image_file_b64) == 0:
            return JSONResponse(content=error_dict("Empty image"), status_code=400)
        try:
            image = Image.open(
                io.BytesIO(base64.b64decode(parameters.image_file_b64))
            )
        except BaseException:
            return JSONResponse(
                content=error_dict("Error decode image!"), status_code=400
            )
    elif parameters.image_url:
        if not (
            parameters.image_url.startswith("http://")
            or parameters.image_url.startswith("https://")
        ) or is_loopback(parameters.image_url):
            print(
                f"Possible ssrf attempt to /api/removebg endpoint with image url: {parameters.image_url}"
            )
            return JSONResponse(
                content=error_dict("Invalid image url."), status_code=400
            )  # possible ssrf attempt
        try:
            image = Image.open(
                io.BytesIO(requests.get(parameters.image_url).content)
            )
        except BaseException:
            return JSONResponse(
                content=error_dict("Error download image!"), status_code=400
            )
    if image is None:
        return JSONResponse(
            content=error_dict("Error download image!"), status_code=400
        )

    config: WebAPIConfig = init_config()
    interface = init_interface(config)
    result = process_remove_bg(
                    interface, parameters.dict(), image, bg, False
                )
    # return handle_response(result, image)
    return {"maskImage": result["data"][0].decode('utf-8')}

    # return parameters

# This must be included for the serverless to work.
runpod.serverless.start({"handler": is_even})  # Required
