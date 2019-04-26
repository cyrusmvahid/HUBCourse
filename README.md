# Course Description
# Environmnet set up
To install git on your Windows laptop please watch: https://www.youtube.com/watch?v=albr1o7Z1nw
To install conda on your Windows laptop please watch: https://www.youtube.com/watch?v=dWeWCQmewLc

To install Conda please refer to [this link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
```
 conda create -n HUB python=3.6 anaconda
 source activate HUB
 pip install numpy mxnet jupyter seaborn matplotlib pandas scipy gluoncv gluonnlp scikit-learn
 #test your environment
 which python
 # shoud result in <your conda path>//envs/HUB/bin/python
 python --version
 #Python 3.6.8 :: Anaconda, Inc.
 #To leave the environment
 conda deactivate
 ```
# References
- for self-learning python refer to: https://www.learnpython.org/
- for self-learning python and numpy refer to: https://www.datacamp.com/home
- for more details on deep learning refer to: http://d2l.ai 
