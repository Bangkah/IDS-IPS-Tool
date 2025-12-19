from setuptools import setup, find_packages

setup(
    name="ids-ips-tool",
    version="1.0.1",
    description="Modular IDS/IPS Tool with Real-time Dashboard",
    author="Bangkah",
    author_email="mdhyaulatha@gmail.com",
    url="https://github.com/Bangkah/IDS-IPS-Tool",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "scapy",
        "watchdog",
        "notify2",
        "fastapi",
        "uvicorn",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "ids_main=ids_main:main",
            "ips_main=ips_main:main",
            "netids_main=netids_main:main"
        ]
    },
    include_package_data=True,
    package_data={
        "": [
            "../dashboard/templates/*.html",
            "../dashboard/static/*.css",
            "../dashboard/static/*.js",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)