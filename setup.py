from distutils.core import setup
include_package_data = True
setup(
    name='Barakis',
    packages=['barakis'],
    version='7.2.1.3',
    license='MIT',
    description='bot for the popular browsergame ogame',
    author='PapeprPieceCode',
    author_email='marcos.gam@hotmail.com',
    url='https://github.com/PiecePaperCode/Barakis',
    download_url='https://github.com/PiecePaperCode/Barakis.git',
    keywords=['OGame', 'bots', 'bot'],
    install_requires=['flask', 'ogame', 'gevent'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)