from __future__ import annotations

from typing import Any


def build_location_label(geo: dict[str, Any] | None) -> str | None:
    geo = geo or {}

    city = geo.get("city")
    region = geo.get("region")
    country = geo.get("country") or geo.get("country_code")

    if city and country:
        return f"{city}, {country}"
    if region and country:
        return f"{region}, {country}"
    if country:
        return str(country)

    return None


def build_provider_label(org: str | None, geo: dict[str, Any] | None) -> str | None:
    geo = geo or {}
    return org or geo.get("as_org") or geo.get("organization")


def build_connection_type_label(
    ip_data: dict[str, Any] | None,
    geo: dict[str, Any] | None,
) -> str | None:
    ip_data = ip_data or {}
    geo = geo or {}

    if ip_data.get("is_tor"):
        return "Tor"
    if ip_data.get("is_vpn"):
        return "VPN"
    if ip_data.get("is_proxy"):
        return "Proxy"
    if ip_data.get("is_hosting"):
        return "Hosting"

    connection_type = geo.get("connection_type")
    if connection_type == "hosting":
        return "Hosting"
    if connection_type == "residential":
        return "Direct"

    method = ip_data.get("detection_method")
    if method in {"x_forwarded_for", "forwarded", "x_real_ip"}:
        return "Proxy"
    if method in {"direct", "direct_fallback"}:
        return "Direct"

    return None


def build_coordinates_label(geo: dict[str, Any] | None) -> str | None:
    geo = geo or {}

    lat = geo.get("latitude")
    lon = geo.get("longitude")

    if lat is None or lon is None:
        return None

    return f"{lat}, {lon}"


def build_ip_version_label(ip_data: dict[str, Any] | None) -> str | None:
    ip_data = ip_data or {}
    return ip_data.get("ip_version")


def build_network_summary(
    current_ip: str | None,
    current_ip_data: dict[str, Any] | None,
    current_port: int | None,
    geo: dict[str, Any] | None,
    org: str | None,
    asn: str | None,
) -> dict[str, Any]:
    ip_data = current_ip_data or {}
    geo = geo or {}

    return {
        "current_ip": current_ip,
        "current_ip_data": ip_data,
        "current_port": current_port,
        "geo": geo,
        "asn": asn,
        "org": org,
        "location_label": build_location_label(geo),
        "provider_label": build_provider_label(org, geo),
        "connection_type_label": build_connection_type_label(ip_data, geo),
        "coordinates_label": build_coordinates_label(geo),
        "ip_version_label": build_ip_version_label(ip_data),
    }