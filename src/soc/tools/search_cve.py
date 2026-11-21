from .common import PROJECT, load_json, validate_string, record_tool_call


def search_cve(product):
    inputs = {"product": product}

    try:
        product = validate_string(product, "product")

        path = PROJECT / "data" / "intelligence" / "cve_catalog.json"
        catalogue = load_json(path)

        if not isinstance(catalogue, list):
            raise ValueError("CVE catalogue must contain a JSON list")

        matches = []

        for item in catalogue:
            if not isinstance(item, dict):
                continue

            item_product = item.get("product")
            if not isinstance(item_product, str):
                continue

            if item_product.casefold() == product.casefold():
                matches.append(item)

        output = {
            "success": True,
            "tool": "search_cve",
            "product": product,
            "count": len(matches),
            "matches": matches,
            "source_type": "local_mock_catalogue",
            "live_lookup_performed": False,
            "message": (
                "Matching catalogue entries found"
                if matches else "No matching catalogue entries found"
            )
        }

        record_tool_call("search_cve", inputs, output, "success")
        return output

    except Exception as exc:
        output = {
            "success": False,
            "tool": "search_cve",
            "error": str(exc),
            "matches": [],
            "live_lookup_performed": False
        }
        record_tool_call("search_cve", inputs, output, "failure")
        return output
