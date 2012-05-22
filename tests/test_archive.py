import os

from tarfile import TarFile
from zipfile import ZipFile

import pytest

from flexmock import flexmock

from pyp2rpmlib.archive import Archive

tests_dir = os.path.split(os.path.abspath(__file__))[0]

class TestArchive(object):
    td_dir = '%s/test_data/' % tests_dir

    def setup_method(self, method):
        # create fresh archives for every test

        self.a = [Archive('%splumbum-0.9.0.tar.gz' % self.td_dir),
                  Archive('%spytest-2.2.3.zip' % self.td_dir),
                  Archive('%srestsh-0.1.tar.gz' % self.td_dir),
                  Archive('%sSphinx-1.1.3-py2.6.egg' % self.td_dir),
                  Archive('%sunextractable-1.tar' % self.td_dir),
                  Archive('%sbitarray-0.8.0.tar.gz' % self.td_dir),
                 ]

    @pytest.mark.parametrize(('i', 'expected'), [
        (0, TarFile),
        (1, ZipFile),
        (2, TarFile),
        (3, ZipFile),
        (4, TarFile),
    ])
    def test_extractor_cls(self, i, expected):
        assert self.a[i].extractor_cls == expected

    @pytest.mark.parametrize(('i', 'n', 'abs', 'expected'), [
        (0, 'setup.cfg', False, '[egg_info]\r\ntag_build = \r\ntag_date = 0\r\ntag_svn_revision = 0\r\n\r\n'),
        (1, 'requires.txt', False, 'py>=1.4.7.dev2'),
        (1, 'pytest-2.2.3/pytest.egg-info/requires.txt', True, 'py>=1.4.7.dev2'),
        (2, 'does_not_exist.dne', False,  None),
        (4, 'in_unextractable', False, None),
    ])
    def test_get_content_of_file_from_archive(self, i, n, abs, expected):
        with self.a[i] as a:
            assert a.get_content_of_file(n, abs) == expected

    def test_find_list_argument_not_present(self):
        flexmock(self.a[4]).should_receive('get_content_of_file').with_args('setup.py').and_return('install_requires=["spam",\n"eggs"]')
        assert self.a[4].find_list_argument('setup_requires') == []

    def test_find_list_argument_present(self):
        flexmock(self.a[4]).should_receive('get_content_of_file').with_args('setup.py').and_return('install_requires=["beans",\n"spam"]\nsetup_requires=["spam"]')
        assert self.a[4].find_list_argument('install_requires') == ['beans', 'spam']

    def test_find_list_argument_unopenable_file(self):
        flexmock(self.a[4]).should_receive('get_content_of_file').with_args('setup.py').and_return(None)
        assert self.a[4].find_list_argument('install_requires') == []

    @pytest.mark.parametrize(('i', 'suf', 'expected'), [
        (0, ['.spamspamspam'],  False),
        (1, '.py', True),
        (4, ['.eggs'], False),
    ])
    def test_has_file_with_suffix(self, i, suf, expected):
        with self.a[i] as a:
            assert a.has_file_with_suffix(suf) == expected
