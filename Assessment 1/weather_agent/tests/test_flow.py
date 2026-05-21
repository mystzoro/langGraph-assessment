from unittest.mock import patch


def mocked_get(url, params=None, timeout=None):
    class MockResponse:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

        def raise_for_status(self):
            return None

    if 'ipapi.co' in url:
        return MockResponse({
            'city': 'Test City',
            'region': 'Test Region',
            'country_name': 'Testland',
            'latitude': '10.0',
            'longitude': '20.0',
            'utc_offset': '+00:00',
            'timezone': 'UTC'
        })
    if 'open-meteo.com' in url:
        return MockResponse({
            'latitude': 10.0,
            'longitude': 20.0,
            'timezone': 'UTC',
            'utc_offset_seconds': 0,
            'current_weather_units': {
                'temperature': '°C',
                'windspeed': 'km/h',
                'winddirection': 'deg',
                'weathercode': 'code'
            },
            'current_weather': {
                'time': '2026-05-21T05:15:00Z',
                'temperature': 15.5,
                'windspeed': 5.0,
                'winddirection': 180,
                'is_day': 1,
                'weathercode': 0
            }
        })

    raise ValueError(f"Unhandled URL in test mock: {url}")


@patch('components.nodes.requests.get', side_effect=mocked_get)
def test_full_agent_flow(mock_get):
    # Import here so the patch is in effect for module-level calls
    from graph import weather_agent

    state = {'name': 'Tester', 'location_data': None, 'weather_data': None, 'weather_info': None}

    final = weather_agent.invoke(state)

    assert final is not None
    assert 'weather_info' in final
    assert final['weather_info'] is not None
    assert 'Test City' in final['weather_info']
    assert 'Temperature' in final['weather_info']
