# Goals of this session

Our audiance here is data scientists who knows python and sql.
They are trying hitting OOM errors and want to optimize their ML models, usually they won't be very comfortable with infra side of things and so will be new to GPU programming.

We show them how to convert the current pandas code into using GPU. Because this is the main usecases we come across in the industry. They won't be directly using PyTorch for data manipulation. 

In another submodule let us show how model training can be done using GPU. Pick a very simple model and create the requried dataset for it to be trained on also. Then we show write the training code using GPU. We don't go into details of the model. We just show how to use GPU for training. It will have the basic linear regression and training for 10 epochs.This will be a very simple model and we will show how to use GPU for training.

### What we will learn?
- Based on above scenario we explain how tensors are used in torch, the difference between tensors and numpy arrays.
- How can they start leveraging GPU for thier pandas like operations and how to convert their current code to use GPU.

### What we won't learn?
- CUDA programming
- hardware details
- memory hierarchy details

# Make sure to reference the /Users/raghunandanask/Desktop/github-repo/gpu-training/teaching_style.md file for the teaching style.