import copy
import datetime

from src.AoC_app import LeaderBoard

TEST_RESPONSE = {
    "1": {
        "id": 1,
        "local_score": 10,
        "name": "Ola Nordmann",
        "completion_day_level": {"1": {"1": {"get_star_ts": 1669980131}}},
        "last_star_ts": 1669980754,
    }
}


def test_update_second_star():

    leader_board = LeaderBoard()
    assert leader_board.update_board(copy.deepcopy(TEST_RESPONSE)) == {}

    update = copy.deepcopy(TEST_RESPONSE)
    update["1"]["completion_day_level"]["1"]["2"] = {"get_star_ts": 1669980900}
    update["1"]["last_star_ts"] = 1669980900
    result = leader_board.update_board(update)

    expected_result = {
        datetime.datetime(2022, 12, 2, 12, 35): {
            "name": "Ola Nordmann",
            "day": "1",
            "star": "2",
        }
    }
    assert result == expected_result


def test_update_second_day():

    leader_board = LeaderBoard()
    assert leader_board.update_board(copy.deepcopy(TEST_RESPONSE)) == {}

    update = copy.deepcopy(TEST_RESPONSE)
    update["1"]["completion_day_level"]["2"] = {"1": {"get_star_ts": 1669980900}}
    update["1"]["last_star_ts"] = 1669980900
    result = leader_board.update_board(update)

    expected_result = {
        datetime.datetime(2022, 12, 2, 12, 35): {
            "name": "Ola Nordmann",
            "day": "2",
            "star": "1",
        }
    }
    assert result == expected_result
