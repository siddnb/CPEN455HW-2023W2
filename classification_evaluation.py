'''
This code is used to evaluate the classification accuracy of the trained model.
You should at least guarantee this code can run without any error on validation set.
And whether this code can run is the most important factor for grading.
We provide the remaining code, all you should do are, and you can't modify the remaining code:
1. Replace the random classifier with your trained model.(line 64-68)
2. modify the get_label function to get the predicted label.(line 18-24)(just like Leetcode solutions)
'''
from torchvision import datasets, transforms
from utils import *
from model import * 
from dataset import *
from tqdm import tqdm
from pprint import pprint
import argparse
NUM_CLASSES = len(my_bidict)

# Write your code here
# And get the predicted label, which is a tensor of shape (batch_size,)
# Begin of your code
def get_label(model, model_input, device, save_logits = False):
    # Run the model 4 times with the input and the 4 possible labels
    # Create a tensor of shape (batch_size, 4) with the output of the model
    # Get the index of the maximum value for each batch
    # Return the index as a tensor of shape (batch_size,)
    answers = None
    
    # Used github copilot in this function
    for _, label_num in my_bidict.items():
        categories = torch.tensor([label_num]*model_input.shape[0]).to(device)
        categories = categories.to(device)

        model_output = model(model_input, categories)
        answer = image_discretized_mix_logistic_loss(model_input, model_output)

        # CHANGE TO PASS INTO LOSS FUNCTION FOR EACH IMAGE
        # BELOW ONLY OUTPUTS DISTIRBUTION, NOT LOSS
        # answer = model(model_input, categories)
        if label_num == 0:
            answers = answer.unsqueeze(1)
        else:
            answers = torch.cat((answers, answer.unsqueeze(1)), dim=1)
    logits = answers
    answer = torch.argmin(answers, dim=1)

    if save_logits:
        return answer, logits
    else:
        return answer
# End of your code

def classifier(model, data_loader, device):
    model.eval()
    acc_tracker = ratio_tracker()
    for batch_idx, item in enumerate(tqdm(data_loader)):
        model_input, categories = item
        model_input = model_input.to(device)
        original_label = [my_bidict[item] for item in categories]
        original_label = torch.tensor(original_label, dtype=torch.int64).to(device)
        answer = get_label(model, model_input, device)
        correct_num = torch.sum(answer == original_label)
        acc_tracker.update(correct_num.item(), model_input.shape[0])
    
    return acc_tracker.get_ratio()

'''Added code here to write to csv for submission'''
def submit_classifier(model, data_loader, device, batch_size):
    write_to_csv = []
    write_to_npy = []
    model.eval()
    acc_tracker = ratio_tracker()
    for batch_idx, item in enumerate(tqdm(data_loader)):
        model_input, categories = item
        model_input = model_input.to(device)
        
        answer, logits = get_label(model, model_input, device, save_logits=True)
        
        write_to_csv[batch_idx*batch_size:(batch_idx+1)*batch_size] = answer.tolist()
        write_to_npy[batch_idx*batch_size:(batch_idx+1)*batch_size] = logits.tolist()
    
    csv_file_path = 'submission.csv'
    with open(csv_file_path, 'w') as csvfile:
        for row in write_to_csv:
            # Convert each element to a string and join them with commas
            # Write the row string to the file
            csvfile.write(' ,' + str(row) + '\n')
    np.save('test_logits.npy', write_to_npy)
    return 0        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--data_dir', type=str,
                        default='data', help='Location for the dataset')
    parser.add_argument('-b', '--batch_size', type=int,
                        default=32, help='Batch size for inference')
    parser.add_argument('-m', '--mode', type=str,
                        default='validation', help='Mode for the dataset')
    
    args = parser.parse_args()
    pprint(args.__dict__)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("mps" if torch.backends.mps.is_available() else device)
    kwargs = {'num_workers':0, 'pin_memory':True, 'drop_last':True}

    ds_transforms = transforms.Compose([transforms.Resize((32, 32)), rescaling])
    dataloader = torch.utils.data.DataLoader(CPEN455Dataset(root_dir=args.data_dir, 
                                                            mode = args.mode, 
                                                            transform=ds_transforms), 
                                             batch_size=args.batch_size, 
                                            #  shuffle=True, 
                                            shuffle = False,
                                             **kwargs)

    #Write your code here
    #You should replace the random classifier with your trained model
    #Begin of your code
    model = PixelCNN(nr_resnet=2, nr_filters=40, input_channels=3, nr_logistic_mix=5)
    #End of your code
    
    model = model.to(device)
    #Attention: the path of the model is fixed to 'models/conditional_pixelcnn.pth'
    #You should save your model to this path
    # model.load_state_dict(torch.load('models/conditional_pixelcnn.pth'))
    model.eval()
    print('model parameters loaded')
    # acc = classifier(model = model, data_loader = dataloader, device = device)
    acc = submit_classifier(model = model, data_loader = dataloader, device = device, batch_size = args.batch_size)
    print(f"Accuracy: {acc}")
        
        