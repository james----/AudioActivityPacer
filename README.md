# Audio Activity Pacer

## Python script to help you do exercise repetitions or anything else that needs an audio file of incremental counts with user defined increments of silence.

### Syntax

```python activity_pacer.py <max_count> <duration_1> <duration_2>```
| Parameter           | Type         | Description                                        |
| ------------------- | ------------ | -------------------------------------------------- |
| `max_count`         | `int`        | **Required.** The highest number to count to.      |
| `silence_durations` | `list[int]`  | **Required.** One or more integers representing seconds of silence, separated by spaces. |


Example creates an audio file that has 10 reps where each rep has three periods of silence the first taking 5 seconds the second taking 10 and the last taking 5 seconds.

```python activity_pacer.py 10 5,10,5```
