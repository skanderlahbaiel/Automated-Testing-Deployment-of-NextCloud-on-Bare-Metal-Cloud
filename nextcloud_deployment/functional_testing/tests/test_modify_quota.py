from functional_testing.utils.user_management import modify_quota, test_quota
from functional_testing.config.configuration import (
    MODIFY_USER_BUTTON_XPATH,
    SAVE_MODIFICATION_BUTTON_XPATH
)




def modify_user_quota(driver, username, quota, password):
    """modiy_user_quota _summary_

    _extended_summary_

    :param driver: _description_
    :type driver: _type_
    """
    try:
        modify_quota(driver, username, quota, MODIFY_USER_BUTTON_XPATH, SAVE_MODIFICATION_BUTTON_XPATH)
        test_quota(driver, username, password)
        return True
    except Exception as e:
        print(f"An error occurred while modifying user quota: {e}")
        raise