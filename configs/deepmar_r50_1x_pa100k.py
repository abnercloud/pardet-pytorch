# model
model = dict(
    type='DeepMAR',
    backbone=dict(
        type='ResNet50',
        layers=(3, 4, 6, 3),
        pretrained=True,
    ),
    classifier=dict(
        type='BaseClassifier',
        nattr=26,
    ),
    loss=dict(
        type='CEL_Sigmoid',
        sample_weight=None,
        size_average=True
    ),
)
train_cfg = dict(
    train_cfg='',
)
test_cfg = dict(
    test_cfg='',
)

# data
dataset_type = 'PA100K'
data_root = '/pardet-pytorch/data/PA100K/'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
train_pipeline = [
    dict(type='Resize', size=(256, 192)),
    dict(type='Pad', padding=10),
    dict(type='RandomCrop', size=(256, 192)),
    dict(type='RandomHorizontalFlip', p=0.5),
    dict(type='ToTensor'),
    dict(type='Normalize', **img_norm_cfg),
]
test_pipeline = [
    dict(type='Resize', size=(256, 192), keep_ratio=True),
    dict(type='ToTensor'),
    dict(type='Normalize', **img_norm_cfg),
]
data = dict(
    batchsize=64,
    workers=8,
    shuffle=True,
    train=dict(
        type=dataset_type,
        split='train',
        ann_file=data_root + 'annotation/train.pkl',
        img_prefix=data_root + 'data/release_data/release_data/',
        pipeline=train_pipeline
    ),
    val=dict(
        type=dataset_type,
        split='val',
        ann_file=data_root + 'annotations/val.pkl',
        img_prefix=data_root + 'data/release_data/release_data/',
        pipeline=train_pipeline
    ),
    test=dict(
        type=dataset_type,
        split='test',
        ann_file=data_root + 'annotations/test.pkl',
        img_prefix=data_root + 'data/release_data/release_data/',
        pipeline=test_pipeline
    )
)
evaluation = dict(interval=1, metric='mA')

# optimizer
optimizer = dict(
    type='SGD', lr=0.01, momentum=0.9, weight_decay=5e-4,
    constructor='DefaultOptimizerConstructor',
    paramwise_cfg=dict(
        custom_keys={
            '.backbone': dict(lr_mult=1),
            '.classifier': dict(lr_mult=10)
        }
    )
)
optimizer_config = dict(
    grad_clip=dict(
        max_norm=10.0,
        norm_type=2)
)
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.001,
    step=[8, 11])
total_epochs = 12

# logs
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        dict(type='TensorboardLoggerHook')
    ])
# ckpts
checkpoint_config = dict(interval=1)

# misc
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1), ('val', 1)]
