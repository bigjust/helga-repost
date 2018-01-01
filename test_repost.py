import datetime
import mock

from helga_repost import check_url, clean_url


class TestPlugin(object):

    def setUp(self):
        pass

    def test_clean_utm_url(self):

        utm_url = 'http://example.com?utm_tag1=athing&utm_tag2=anotherthing&id=5'
        cleaned_url = clean_url(utm_url)

        assert cleaned_url == 'http://example.com?id=5'

    def test_clean_already_clean_url(self):

        url = 'http://example.com'
        cleaned_url = clean_url(url)

        assert cleaned_url == url

    @mock.patch('helga_repost.db')
    def test_check_url_new(self, mock_db):

        db = mock_db.repost.find.return_value
        db.sort.return_value = [{
            'channel': '#test',
            'nick': 'othernick',
            'url': 'http://www.example.com',
            'timestamp': datetime.datetime.utcnow(),
        }]

        url = 'http://www.example.com'
        check_result = check_url('#test', 'helga', url)

        assert check_result is None

    @mock.patch('helga_repost.db')
    def test_check_url_repost(self, mock_db):
        url = 'http://www.example.com'

        db = mock_db.repost.find.return_value
        db.sort.return_value = [{
            'channel': '#test',
            'nick': 'nick',
            'url': url,
            'timestamp': datetime.datetime.utcnow(),
        },{
            'channel': '#test',
            'nick': 'othernick',
            'url': url,
            'timestamp': datetime.datetime.utcnow(),
        }]

        result = check_url('#test', 'helga', url)

        assert result is not None
        assert 'nick' == result[0]

    @mock.patch('helga_repost.db')
    def test_same_nick_exception(self, mock_db):
        url = 'http://www.example.com'

        db = mock_db.repost.find.return_value
        db.sort.return_value = [{
            'channel': '#test',
            'nick': 'nick',
            'url': url,
            'timestamp': datetime.datetime.utcnow(),
        },{
            'channel': '#test',
            'nick': 'nick',
            'url': url,
            'timestamp': datetime.datetime.utcnow(),
        }]

        checked_url = check_url('#test', 'nick', url)

        assert checked_url is None
