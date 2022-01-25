import unittest
import gc
import os
import time
from trender import TRender
from trender import (
    MacroOrBlockNotDefinedError,
    MacroOrBlockExistError,
    UnexpectedBlockError,
    UnexpectedEOFError,
    DefineBlockError,
    TemplateNotExistsError,
    MacroBlockUsageError)


TEMPLATES_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'templates')


class TestTRender(unittest.TestCase):

    def setUp(self):
        gc.collect()

    def test_escaping(self):
        template = '{curly} and @!escaped'
        expecting = template.replace('@!', '@')
        result = TRender(template).render()
        self.assertEqual(result, expecting)

    def test_simple_var(self):
        template = '@name@!@domain'
        expecting = 'iris@here.nl'
        result = TRender(template).render({
            'name': 'iris',
            'domain': 'here.nl'})
        self.assertEqual(result, expecting)

    def test_for_loop(self):
        template = '''
        #for @person in @people:
            @person.name
        #end'''
        expecting = '''
            Iris
            Sasha'''
        result = TRender(template).render({
            'people': [
                {'name': 'Iris'},
                {'name': 'Sasha'}]})
        self.assertEqual(result, expecting)

    def test_simple_if(self):
        template = '''
        #if @foo:
            Hooray
        #end'''
        expect_true = '''
            Hooray'''
        result = TRender(template).render({'foo': True})
        self.assertEqual(result, expect_true)

        expect_false = ''
        result = TRender(template).render({'foo': False})
        self.assertEqual(result, expect_false)

    def test_if_by_function(self):
        template = '''
        #if @is_green(@color):
            grass
        #elif @is_blue(@color):
            sky
        #else:
            @color
        #end'''
        namespace = {
             'is_green': lambda color: color == 'green',
             'is_blue': lambda color: color == 'blue'}

        expect_green = '''
            grass'''
        namespace['color'] = 'green'
        self.assertEqual(TRender(template).render(namespace), expect_green)

        expect_blue = '''
            sky'''
        namespace['color'] = 'blue'
        self.assertEqual(TRender(template).render(namespace), expect_blue)

        expect_purple = '''
            purple'''
        namespace['color'] = 'purple'
        self.assertEqual(TRender(template).render(namespace), expect_purple)

    def test_comments(self):
        template = '''
        # This is comment
        #
        # Above is an empty comment, let's check if we see that as a comment
        This is not
        ## This is comment too'''
        expecting = '''
        This is not'''
        self.assertEqual(TRender(template).render(), expecting)

    def test_macro(self):
        template = '''
        #macro NI:
        @ni
        #end
        #for @ni in @range:
            #NI
        #end'''
        expecting = '''
        ni
        ni
        ni'''
        self.assertEqual(TRender(template).render(
            {'range': range(3), 'ni': 'ni'}), expecting)

    def test_block(self):
        template = '''
        #block Ni:
        @ni
        #end
        #for @ni in @range:
            #Ni
        #end'''
        expecting = '''
        0
        1
        2'''
        self.assertEqual(TRender(template).render(
            {'range': range(3), 'ni': 'ni'}), expecting)

    def test_render_exceptions(self):
        with self.assertRaises(MacroOrBlockNotDefinedError):
            TRender('#NOT_DEFINED').render()

        with self.assertRaises(MacroOrBlockExistError):
            TRender('''
            #macro FOO:
            #end
            #macro FOO:
            #end''').render()

    def test_compile_exceptions(self):
        with self.assertRaises(UnexpectedBlockError):
            TRender('#else')

        with self.assertRaises(UnexpectedEOFError):
            TRender('#if @foo:')

        with self.assertRaises(UnexpectedEOFError):
            TRender('#if @foo:')

        with self.assertRaises(DefineBlockError):
            TRender('#if @foo')  # missing :

        with self.assertRaises(DefineBlockError):
            TRender('#if @foo')  # missing :

        with self.assertRaises(TemplateNotExistsError):
            TRender('dummy', path='.')

        with self.assertRaises(TemplateNotExistsError):
            TRender('dummy', path='.')

        with self.assertRaises(MacroBlockUsageError):
            TRender('''
            #macro FOO:
            #end
            #FOO:''')  # : should not be added to FOO

        # we allow garbage during compile errors due to traceback.
        # when you expect compiles to fail in a production env
        # you should catch these exceptions and set __traceback__
        # to None.
        gc.collect()

    def test_extend(self):
        expecting = '''
<body>
test extend
</body>'''
        result = TRender('test_extend.template', TEMPLATES_PATH).render()
        self.assertEqual(result, expecting)

    def test_include(self):
        expecting = '''
<body>
test include
</body>'''
        result = TRender('test_include.template', TEMPLATES_PATH).render()
        self.assertEqual(result, expecting)

    def test_simple_performance(self):
        template = '''
        #if @test:
            test is true
        #else:
            test is false
        #end
        #block Person:
        name: @person.name
        #end
        #for @person in @people:
            #Person
        #end'''
        namespace = {
            'test': True,
            'people': [
                {'name': 'Iris'},
                {'name': 'Sasha'}]}
        compiled = TRender(template)
        start = time.time()
        for _ in range(10 ** 4):
            compiled.render(namespace)
        finished = time.time() - start
        # This should be easy below 1.0, even on slower computers
        self.assertLess(finished, 1.0)

    def tearDown(self):
        self.assertEqual(gc.collect(), 0, msg=self.id())


if __name__ == '__main__':
    unittest.main()
