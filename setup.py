from setuptools import setup

setup(
    name='translator_tool',
    version='0.1',
    py_modules=['translator'],
    install_requires=['Pillow==10.4.0',
        'PyAutoGUI==0.9.54',
        'pytesseract==0.3.10',
        'torch==2.4.0+cu124',
        'transformers==4.43.3',
    ],
    entry_points={
        'console_scripts': [
            'translator=translator:main',
        ]
    },
    author='Julien Lapierre',
    author_email='Julien.Lapierre@hotmail.ca',
    description='Little jpn/ch translator tool using tkinter,pytesseract,MarianMT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Crimsonchamp/Translator_Tool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
)