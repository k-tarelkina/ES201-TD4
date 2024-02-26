# Automated script for analysing cache performance using SimplScalar

## Prerequisites

You may need to install some dependencies first.

```
sudo apt install zip unzip
```

## Run the sript

Clone this repo:

```
git clone https://github.com/k-tarelkina/ES201-TD4.git
```

Copy the script to the directory with your executables:

```
cp ./ES201-TD4/cache_metrics.py /path/to/executables
```

Go to the directory with your executables:

```
cd /path/to/executables
```

Execute script:

```
python ./cache_metrics.py [processor: cortex_a15 or cortex_a7] [paths_to_executables]
```

Make sure to run script for both processor configurations, e.g.:

```
python ./cache_metrics.py cortex_a15 <prog>.ss
python ./cache_metrics.py cortex_a7 <prog>.ss
```

## Upload results

Copy generated archive with plots to the repo directory:

```
cp plots.zip /path/to/ES201-TD4/repo
```

Go to the repo:

```
cd /path/to/ES201-TD4/repo
```

Use your github credentials to upload results to the repo:

```
git add .
git commit -m 'Add plots'
git push
```
