from distutils.core import setup

setup(
    name = "pyscooter",
    packages = ["pyscooter"],
    version = "0.1",
    license = "MIT",
    description = "Python library to use rentable scooters without the official app.",
    author = "BastelPichi",
    author_email = "pichi@pichisdns.com",
    url = "https://github.com/BastelPichi/pyscooter",
    download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords = ["Scooter", "Rent", "Bolt"],
    install_requires=[
        "requests"
    ]
)
