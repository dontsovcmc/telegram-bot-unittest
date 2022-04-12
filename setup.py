import os
from setuptools import setup

VERSION_MAJOR = 0
VERSION_MINOR = 1

ver = '%d.%d' % (VERSION_MAJOR, VERSION_MINOR)

if __name__ == '__main__':
    """
    Create Packet:

    python setup.py sdist --formats=zip bdist_wheel   # или --formats=gztar
    twine upload dist/*
    """
    with open(os.path.join(os.getcwd(), 'README.rst'), 'r', encoding='utf-8') as fh:
        long_description = fh.read()

    setup(
        name='telegram-bot-unittest',
        version=ver,
        description='test your python-telegram-bot easily',
        long_description=long_description,
        long_description_content_type='text/x-rst',
        author='Dontsov E.',
        author_email='dontsovcmc@gmail.com',
        url='https://github.com/dontsovcmc/telegram_bot_unittest',
        include_package_data=True,
        packages=[
            'echobot',
            'telegram_bot_unittest'
        ],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Communications :: Chat',
            'Topic :: Internet',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        python_requires='>=3.6',
        license='LGPLv3',
        install_requires=[
            'python-telegram-bot',
            'pytest',
            'pytest-cov',
            'flask',
            'waitress'
        ],
    )
