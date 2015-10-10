import os
from unittest import mock
import sys
import shutil
import tempfile
from pyramid.compat import NativeIO
from djed.templates import script as layer
from djed.templates.layer import ID_LAYER

from .base import BaseTestCase


class TestPlayerCommand(BaseTestCase):

    def setUp(self):
        super(TestPlayerCommand, self).setUp()

        self.dir = tempfile.mkdtemp()
        self.stdout = sys.stdout
        sys.stdout = self.out = NativeIO()

    def tearDown(self):
        shutil.rmtree(self.dir)
        sys.stdout = self.stdout
        super(TestPlayerCommand, self).tearDown()

    @mock.patch('djed.templates.script.bootstrap')
    def test_no_params(self, m_bs):
        m_bs.return_value = {'registry': self.registry}

        sys.argv[:] = ['djed.templates', 'djed.templates.ini']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('[-l [LAYERS [LAYERS ...]]]', val)
        self.assertIn('[-lt [TEMPLATES [TEMPLATES ...]]]', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_list_categories_no_layers(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.registry[ID_LAYER] = {}

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-l']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('No layers are found.', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_list_categories(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.config.add_layer(
            'test1', path='tests:dir1/')
        self.config.add_layer(
            'test2', path='tests:bundle/')

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-l']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('* Layer: test1', val)
        self.assertIn('* Layer: test2', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_list_categories_limit(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.config.add_layer(
            'test1', path='tests:dir1/')
        self.config.add_layer(
            'test2', path='tests:bundle/')

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-l', 'test2']

        layer.main()

        val = self.out.getvalue()
        self.assertNotIn('* Layer: test1', val)
        self.assertIn('* Layer: test2', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_list_templates(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.config.add_layer(
            'test1', path='tests:dir1/')
        self.config.add_layer(
            'test2', path='tests:bundle/')

        def test(): pass

        self.config.add_tmpl_filter(
            'test1:actions', test)

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-lt']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('* Layer: test1', val)
        self.assertIn('tests:dir1/', val)
        self.assertIn('actions: .pt (tests/test_script.py: test)', val)
        self.assertIn('* Layer: test2', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_list_templates_limit(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.config.add_layer(
            'test1', path='tests:dir1/')
        self.config.add_layer(
            'test2', path='tests:bundle/')

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-lt', 'test1']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('* Layer: test1', val)
        self.assertIn('tests:dir1/', val)
        self.assertIn('actions: .pt', val)
        self.assertNotIn('* Layer: test2', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_list_templates_no_layers(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.registry[ID_LAYER] = {}

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-lt']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('No layers are found.', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_customize_template_fmt_bad(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.registry[ID_LAYER] = {}

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-c', 'test', './']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('Template format is wrong.', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_customize_template_no_layers(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.registry[ID_LAYER] = {}
        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-c', 'test:template.lt', './']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('Layer "test" could not be found.', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_customize_template_no_template(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.config.add_layer(
            'test', path='tests:dir1/')

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-c', 'test:template.lt', './']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('Template "test:template.lt" could not be found.', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_customize_template_no_dest(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.config.add_layer(
            'test', path='tests:dir1/')

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-c',
                       'test:view.lt', './blah-blah-blah']

        layer.main()

        val = self.out.getvalue()
        self.assertIn('Destination directory is not found.', val)

    @mock.patch('djed.templates.script.bootstrap')
    def test_customize_success(self, m_bs):
        m_bs.return_value = {'registry': self.registry}
        self.config.add_layer(
            'test', path='tests:dir1/')

        sys.argv[:] = ['djed.templates', 'djed.templates.ini', '-c', 'test:view.lt', self.dir]

        layer.main()

        self.assertTrue(os.path.join(self.dir, 'view.pt'))
