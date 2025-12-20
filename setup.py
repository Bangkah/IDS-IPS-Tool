from setuptools import setup, find_packages

setup(
    name="ids-ips-tool",
    version="1.0.1",
    description="Modular IDS/IPS Tool with Real-time Dashboard",
    author="Bangkah",
    author_email="mdhyaulatha@gmail.com",
    url="https://github.com/Bangkah/IDS-IPS-Tool",
    packages=(
        find_packages(where="src") +
        find_packages(where="dashboard", include=["dashboard", "dashboard.*"]) +
        find_packages(where="firewall", include=["firewall", "firewall.*"])
    ),
    package_dir={"": "src", "dashboard": "dashboard", "firewall": "firewall"},
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
            "ids=src.ids_main:main",
            "ips=src.ips_main:main",
            "netids=src.netids_main:main",
            "firewall=firewall.firewall_main:main"
        ]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires=">=3.7",
)