from setuptools import setup, find_packages

setup(
    name='retail_sales_report',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'pandas',
        'plotly',
        'numpy'
    ],
    package_data={
        'RetailAnalytics': ['sales_data.csv', 'templates/index.html'],
    },
    entry_points={
        'console_scripts': [
            'retail_sales_report=RetailAnalytics.app:main',
        ],
    },
)