# APwD-dataset
APwD dataset is a pair of sounds with differences and text describing the differences. 
It is prepared by Daiki Takeuchi and members in NTT CS lab.
The APwD dataset is designed for research that introduces auxilary textual information into content-based audio retrieval.
Similar sound pairs are synthesized from the existing datasets for audio tagging, FSD50K and ESC50, and the differences are described based on synthesizing method.
For details, please refer to the paper [1].
If you use the APwD dataset in your work, please cite this paper where it was introduced.


[1] Daiki Takeuchi, Yasunori Ohishi, Daisuke Niizumi, Noboru Harada and Kunio Kashino, "Introducing auxiliary text query-modifier to content-based audio retrieval," in Proc of INTERSPEECH, 2022.

<!-- ```
@inproceedings{niizumi2022composing,
    title       = {Introducing auxiliary text query-modifier to content-based audio retrieval},
    author      = {Daiki Takeuchi and Yasunori Ohishi and Daisuke Niizumi and Noboru Harada and Kunio Kashino},
    booktitle   = {2022 INTERSPEECH},
    year        = {2022},
}
``` -->
<!-- Paper URL: https://arxiv.org/hogehogefugafufa -->

## Usage
1. Preparing FSD50K and ESC-50 <br>
Download FSD50K and ESC50. You can download them from the following URLs<br>
FSD50k: https://zenodo.org/record/4060432 <br>
ESC-50: https://github.com/karolpiczak/ESC-50 <br>
After downloading, make a note of the directory where each wav file is saved (it will be used in the next step).

1. Modifying setting <br>
In utils.py, rewrite the contents of the two variables (**FSD50K** and **ESC50**) to your environment
The variables are defined at the beginning of the file as follows: directories FSD50k and ESC-50.
Please enter the directory of the data saved in the previous step.

1. Synthesizing dataset <br>
Run synthesize_dataset.sh.

## License
See the file named LICENSE

## Authors
Daiki Takeuchi <br>
Yasunori Ohishi <br>
Daisuke Niizumi <br>
Noboru Harada <br>
Kunio Kashino <br>
