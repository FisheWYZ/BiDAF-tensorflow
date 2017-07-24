# Bi-directional Attention Flow for Machine Comprehension
 
- This the original implementation of [Bi-directional Attention Flow for Machine Comprehension][paper] (Seo et al., 2016).
- This is tensorflow v1.2.0 comaptible version.
- The CodaLab worksheet for the [SQuAD Leaderboard][squad] submission is available [here][worksheet].
- Please contact [Minjoon Seo][minjoon] ([@seominjoon][minjoon-github]) for questions and suggestions. You may contact [iamgroot42](https://github.com/iamgroot42) as well, I'll try and help ^_^.

## 0. Requirements
#### General
- Python 3
- unzip

#### Python Packages
- tensorflow (deep learning library, verified on 1.2.0)
- nltk (NLP tools, verified on 3.2.1)
- tqdm (progress bar, verified on 4.7.4)
- jinja2 (for visaulization; if you only train and test, not needed)

## 1. Pre-processing
First, prepare data. Donwload SQuAD data and GloVe and nltk corpus
(~850 MB, this will download files to `$HOME/data`):
```
chmod +x download.sh; ./download.sh
```

Second, Preprocess Stanford QA dataset (along with GloVe vectors) and save them in `$PWD/data/squad` (~5 minutes):
```
python3 -m squad.prepro
```

## 2. Training
The model was trained with NVidia Titan X (Pascal Architecture, 2016).
The model requires at least 12GB of GPU RAM.
If your GPU RAM is smaller than 12GB, you can either decrease batch size (performance might degrade),
or you can use multi GPU (see below).
The training converges at ~18k steps, and it took ~4s per step (i.e. ~20 hours).

Before training, it is recommended to first try the following code to verify everything is okay and memory is sufficient:
```
python3 -m basic.cli --mode train --noload --debug
```

Then to fully train, run:
```
python3 -m basic.cli --mode train --noload
```

You can speed up the training process with optimization flags:
```
python3 -m basic.cli --mode train --noload --len_opt --cluster
```
You can still omit them, but training will be much slower.


## 3. Test
To test, run:
```
python3 -m basic.cli
```

Similarly to training, you can give the optimization flags to speed up test (5 minutes on dev data):
```
python3 -m basic.cli --len_opt --cluster
```

This command loads the most recently saved model during training and begins testing on the test data.
After the process ends, it prints F1 and EM scores, and also outputs a json file (`$PWD/out/basic/00/answer/test-####.json`,
where `####` is the step # that the model was saved).
Note that the printed scores are not official (our scoring scheme is a bit harsher).
To obtain the official number, use the official evaluator (copied in `squad` folder) and the output json file:

```
python3 squad/evaluate-v1.1.py $HOME/data/squad/dev-v1.1.json out/basic/00/answer/test-####.json
```

## 4. Demo
You may try your own paragraph and question by pasting your paragraph in the file `SAMPLE_PARAGRAPH` and then running
```
python3 comprehend.py SAMPLE_PARAGRAPH <question>
```
For example, 
```
python3 comprehend.py SAMPLE_PARAGRAPH what is valuable security?
```
Have a look at this file's code if you want to use this model as an API for your own product. Note that this can be optimized further according to your use case (as the model is loaded from memory every time you run this file), so try to use the library like in the file.
## Results

### Dev Data

|          | EM (%) | F1 (%) |
| -------- |:------:|:------:|
| single   | 67.8   | 77.4   |


Refer to [our paper][paper] for more details.
See [SQuAD Leaderboard][squad] to compare with other models.


## Multi-GPU Training & Testing
This model supports multi-GPU training.
If you want to use batch size of 60 (default) but if you have 3 GPUs with 4GB of RAM,
then you initialize each GPU with batch size of 20, and combine the gradients on CPU.
This can be easily done by running:
```
python3 -m basic.cli --mode train --noload --num_gpus 3 --batch_size 20
```

Similarly, you can speed up your testing by:
```
python3 -m basic.cli --num_gpus 3 --batch_size 20 
```
 

[multi-gpu]: https://www.tensorflow.org/versions/r0.11/tutorials/deep_cnn/index.html#training-a-model-using-multiple-gpu-cards
[squad]: http://stanford-qa.com
[paper]: https://arxiv.org/abs/1611.01603
[worksheet]: https://worksheets.codalab.org/worksheets/0x37a9b8c44f6845c28866267ef941c89d/
[minjoon]: https://seominjoon.github.io
[minjoon-github]: https://github.com/seominjoon
[v0.2.1]: https://github.com/allenai/bi-att-flow/tree/v0.2.1
