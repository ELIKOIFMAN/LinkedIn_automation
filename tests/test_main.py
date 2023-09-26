import pytest
import back


class Test_back:
    def test_role_list(self):
        # check that the role list isn't empty
        assert len(back.role_list) > 0, "the list is empty.. write roles inside of 'role_list'"

    def test_user_data(self):
        # here the method checks that you don't forget to enter your password and username
        assert back.user_name != "", "your user name wasn't found, enter your username"
        assert back.password != "", "your password wasn't found, enter your password"
