from setuptools import setup

setup(
	name='bithumb-bot',
	version='0.13',
	packages=['strategy', 'prettyoutput', 'BithumbGlobal'],
	url='https://github.com/bonsai-minter/bithumb-bot',
	license='Copyright [2020] [commaster] Licensed under the Apache License, Version 2.0 (the «License»);',
	author='commaster',
	author_email='admin@mcorp.space',
	description='auto trading bot bithumb',
	entry_points={
		'console_scripts' :
			['bithumb-bot = core.bithumb:__init__']
	}
)
