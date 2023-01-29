

# Project Structure

(For training and prediction, pls refer to phone pic)

1. train1 -> from train.json in out_cv
2. train2 -> from test json in out_cv 
3. train2_label -> from test_label.json in out_ct
4. val -> from test json in out
5. val_label -> from test_label.json in out
6. test -> from final test data


# Step

## Candidate Generation Logics 


1. User history: clicked, carted in the same session  -> 20
   1. [ ] ordered ??
2. Popularity: Most clicked, carted, ordered in the same week -> 20
3. Item similarity based:  -> 60 (20 from each matrix)
   1. 

## Local CV

1. Candidate generation -> recall
2. ReRank -> recall@20

```shell
 python -m src.evaluate --test-labels out/test_labels.jsonl --predictions data/val_candidates.csv
```

# Feature Enginering

1. Item
    1. [ ] in card number
    2. [ ] 
2. user
    1. [ ] 
3. Item-user iteraction
    1.  [ ] whether click/cart/order
    2.  [ ] time from click/cart/order



# TODO
1. [x] log local CV
2. [ ] Ranker modle -> 
   1. [ ] focus on carts model
      1. [ ] whether click
      2. [ ] time from last click
      3. [ ] feature from co-visitation matics
   2. [ ] seperate model for each
      1. [x] dart model
   3. [ ] more features
   4. [x] add validation while training
3. [ ] candiate generation -> basic idea
   1. Basic ideas
      1. carts-order co-visitation - type-weighted
         1. check the relationship between two items based on wheather present within 24h and the same session; assign wights based on typeweight 
         2. [ ] typeweight={0: 1, 1: 6, 2: 3} -> why carts = 6
      2. buy2buy - appear-times-weighted
         1. Basic ideas:
            1. only keep carts and order actions
            2. co-presence within 14 days
            3. weight = 1
      3. click co-visit -> time-weighted  (all three type are clicks)
         1. same as carts-order co-visition, but time-weighted 
   2. [ ] questions
      1. 
   3. [ ] new idea 
4. [ ] word2vec
   1. [x] basic idea of notebooks
   2. [ ] original notebook -> how to apply it?
   3. [ ] attention word embedding
5. [ ] can't install lightgbm in recsys-dataset env
6. 

# Ref

1. [Local CV log](https://docs.google.com/spreadsheets/d/1eV6AEFA9Z3KfsnKGPgC1xGfUo9YoDEQ6xzaP37Q48o0/edit?usp=sharing)