training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size=(64, 64),
                                                 batch_size=32,
                                           class_mode='binary')
test_set = 1

epochsT = 1

classifier.fit_generator(training_set,
                         steps_per_epoch = 8000,
                         epochs = epochsT,
                         validation_data = test_set,
                         validation_steps = 2000)