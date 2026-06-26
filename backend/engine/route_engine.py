def get_route(from_stop: str, to_stop: str):
    return {
        "from": from_stop,
        "to": to_stop,
        "summary": "Testovací spojení",
        "steps": [
            {
                "type": "walk",
                "text": "Dojdi na vhodné nástupiště."
            },
            {
                "type": "public_transport",
                "line": "PID",
                "text": "Použij doporučené spojení veřejnou dopravou."
            },
            {
                "type": "walk",
                "text": "Dojdi pěšky do cíle."
            }
        ],
        "risk": "low",
        "reliability": 95
    }