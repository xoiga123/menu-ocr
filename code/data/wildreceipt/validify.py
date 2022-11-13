with open('openset_train.txt', 'r') as a, open('openset_train_valid.txt', 'w') as b:
    b.write('[\n')
    for line in a:
        b.write(line)
        b.write(',')
    b.write(']')