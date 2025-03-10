# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

# TODO: Assert received request data

from mock import patch, MagicMock
import os

import pytest

from connect.exceptions import ServerError
from connect.models import Asset, Product, TierConfig
from connect.resources import Directory
from .common import Response, load_str


def _get_asset_response():
    return _get_response_from_file('response_asset.json')


def _get_product_response():
    return _get_response_from_file('response_product.json')


def _get_tier_config_response():
    return _get_response_from_file('response_tier_config.json')


def _get_response_from_file(filename):
    return Response(
        ok=True,
        text=load_str(os.path.join(os.path.dirname(__file__), 'data', filename)),
        status_code=200
    )


def _get_array_response(object_response):
    return Response(
        ok=True,
        text='[{}]'.format(object_response.text),
        status_code=200
    )


def _get_bad_response():
    return Response(
        ok=False,
        text='{}',
        status_code=404
    )


@patch('requests.get')
def test_list_assets(get_mock):
    get_mock.return_value = _get_array_response(_get_asset_response())
    assets = Directory().list_assets()
    assert isinstance(assets, list)
    assert len(assets) == 1
    assert isinstance(assets[0], Asset)
    assert assets[0].id == 'AS-9861-7949-8492'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/assets?in(product.id,(CN-631-322-000))',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params=None)


@patch('requests.get')
def test_get_asset(get_mock):
    get_mock.return_value = _get_asset_response()
    asset = Directory().get_asset('AS-9861-7949-8492')
    assert isinstance(asset, Asset)
    assert asset.id == 'AS-9861-7949-8492'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/assets/AS-9861-7949-8492',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'})


@patch('requests.get', MagicMock(return_value=_get_bad_response()))
def test_get_asset_bad():
    with pytest.raises(ServerError):
        Directory().get_asset('AS-9861-7949-8492')


@patch('requests.get')
def test_list_products(get_mock):
    get_mock.return_value = _get_array_response(_get_product_response())
    products = Directory().list_products()
    assert isinstance(products, list)
    assert len(products) == 1
    assert isinstance(products[0], Product)
    assert products[0].id == 'CN-783-317-575'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/products',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'})


@patch('requests.get')
def test_get_product(get_mock):
    get_mock.return_value = _get_product_response()
    product = Directory().get_product('CN-783-317-575')
    assert isinstance(product, Product)
    assert product.id == 'CN-783-317-575'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/products/CN-783-317-575',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'})


@patch('requests.get', MagicMock(return_value=_get_bad_response()))
def test_get_product_bad():
    with pytest.raises(ServerError):
        Directory().get_product('CN-783-317-575')


@patch('requests.get')
def test_list_tier_configs(get_mock):
    get_mock.return_value = _get_array_response(_get_tier_config_response())
    tier_configs = Directory().list_tier_configs()
    assert isinstance(tier_configs, list)
    assert len(tier_configs) == 1
    assert isinstance(tier_configs[0], TierConfig)
    assert tier_configs[0].id == 'TC-000-000-000'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/tier/configs',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'product.id': 'CN-631-322-000'})


@patch('requests.get')
def test_get_tier_config(get_mock):
    get_mock.return_value = _get_tier_config_response()
    tier_config = Directory().get_tier_config('TC-000-000-000')
    assert isinstance(tier_config, TierConfig)
    assert tier_config.id == 'TC-000-000-000'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/tier/configs/TC-000-000-000',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'})


@patch('requests.get', MagicMock(return_value=_get_bad_response()))
def test_get_tier_config_bad():
    with pytest.raises(ServerError):
        Directory().get_tier_config('TC-000-000-000')
