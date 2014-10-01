#deqodr
###a python library to help hip yuppies study the statistics of decoding ldpc stabilizer codes

##installation
Clone the repo, and run `setup.py`:
    
    git clone https://github.com/bcriger/deqodr.git
    cd deqodr
    sudo python setup.py install
If you don't have superuser status, you can also use:
    
    python setup.py install --user
In the unlikely case that `QuaEC` is not installed automatically, you
can do it manually with:

    sudo pip install QuaEC
Again, if you don't have root, you can try (I haven't tested this):

    pip install --install-option="--prefix=$HOME/.local" QuaEC