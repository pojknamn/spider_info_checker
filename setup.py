import setuptools

setuptools.setup(
	name="spider-info-checker",
	version="0.0.11",
	author="pojk",
	description="Checks for correct spiders info",
	url="https://github.com/pojknamn/spider_info_checker",
	packages=setuptools.find_packages(),
	install_requires=['pydantic', 'libcst'],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	project_urls={
		'Source': 'https://github.com/pojknamn/spider_info_checker',
	},
	entry_points={
		'console_scripts': (
			'check_info = spider_info_checker.check_info:main',
		)
	},
	python_requires='>=3.8',
)
