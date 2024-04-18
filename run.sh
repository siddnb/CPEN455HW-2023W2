# python pcnn_train.py \
# --batch_size 16 \
# --sample_batch_size 16 \
# --sampling_interval 50 \
# --save_interval 50 \
# --dataset cpen455 \
# --nr_resnet 1 \
# --nr_filters 40 \
# --nr_logistic_mix 5 \
# --lr_decay 0.999995 \
# --max_epochs 500 \
# --en_wandb True \

# python3 pcnn_train.py \
# --batch_size 16 \
# --sample_batch_size 16 \
# --sampling_interval 50 \
# --save_interval 20 \
# --dataset cpen455 \
# --nr_resnet 1 \
# --nr_filters 40 \
# --nr_logistic_mix 5 \
# --lr_decay 0.999995 \
# --max_epochs 500 \
# --en_wandb True \


python3 pcnn_train.py \
--batch_size 8 \
--sample_batch_size 192 \
--sampling_interval 20 \
--save_interval 50 \
--dataset cpen455 \
--nr_resnet 1 \
--nr_filters 20 \
--nr_logistic_mix 5 \
--lr 0.0002 \
--lr_decay 0.999995 \
--max_epochs 50 \
--en_wandb True \
