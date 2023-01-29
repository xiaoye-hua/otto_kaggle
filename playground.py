#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    playground.py
# @Time:        18/01/2023 19:21
# @Desc:


def suggest_clicks_weight(df):
    """
    Three parts
        1. unique_uids from this session
        2. aid based on click co-visitation matric
        3. top_clicks from test data
    """
    # USER HISTORY AIDS AND TYPES
    aids = df.aid.tolist()
    types = df.type.tolist()
    unique_aids = list(dict.fromkeys(aids[::-1]))

    # features
    type_weight_current_session = []
    click_covisitation_num = []

    # RERANK CANDIDATES USING WEIGHTS
    if len(unique_aids) >= rec_num:
        # most recent action has the highest score
        weights = np.logspace(0.1, 1, len(aids), base=2, endpoint=True) - 1
        aids_temp = Counter()
        # RERANK BASED ON REPEAT ITEMS AND TYPE OF ITEMS
        for aid, w, t in zip(aids, weights, types):
            aids_temp[aid] += w * type_weight_multipliers[t]
        sorted_aids = [k for k, v in aids_temp.most_common(rec_num)]
        type_weight_current_session += [v for k, v in aids_temp.most_common(rec_num)]
        return sorted_aids
    # USE "CLICKS" CO-VISITATION MATRIX get potential aids -> include all of the aid in one list
    aids2 = list(itertools.chain(*[top_20_clicks[aid] for aid in unique_aids if aid in top_20_clicks]))
    # RERANK CANDIDATES based on presence times
    top_aids2 = [aid2 for aid2, cnt in Counter(aids2).most_common(rec_num) if aid2 not in unique_aids]
    # combined unique_aids and top_aids2
    result = unique_aids + top_aids2[:rec_num - len(unique_aids)]
    # If not enough, USE TOP20 TEST CLICKS
    final_aid_lst = result + list(top_clicks)[:rec_num - len(result)]
    type_weight_current_session += [0] * (rec_num - len(type_weight_current_session))
    assert len(final_aid_lst) == len(
        type_weight_current_session), f"{len(final_aid_lst)} VS {len(type_weight_current_session)}"
    return final_aid_lst, type_weight_current_session


def buys_features(df):
    """
    """
    # USER HISTORY AIDS AND TYPES
    aids = df.aid.tolist()
    types = df.type.tolist()
    # UNIQUE AIDS AND UNIQUE BUYS
    unique_aids = list(dict.fromkeys(aids[::-1]))
    df = df.loc[(df['type'] == 1) | (df['type'] == 2)]
    unique_buys = list(dict.fromkeys(df.aid.tolist()[::-1]))
    # RERANK CANDIDATES USING WEIGHTS

    # features
    type_weight_current_session = []
    click_covisitation_num = []
    # if len(unique_aids) >= rec_num:
    weights = np.logspace(0.5, 1, len(aids), base=2, endpoint=True) - 1
    type_weight_dict = Counter()
    # RERANK BASED ON REPEAT ITEMS AND TYPE OF ITEMS
    for aid, w, t in zip(aids, weights, types):
        type_weight_dict[aid] += w * type_weight_multipliers[t]
        # sorted_aids = [k for k, v in type_weight_dict.most_common(rec_num)]
        # type_weight_current_session += [v for k, v in type_weight_dict.most_common(rec_num)]
        # return sorted_aids

    # USE "CART ORDER" CO-VISITATION MATRIX
    aids2 = list(itertools.chain(*[top_20_buys[aid] for aid in unique_aids if aid in top_20_buys]))
    # USE "BUY2BUY" CO-VISITATION MATRIX
    aids3 = list(itertools.chain(*[top_20_buy2buy[aid] for aid in unique_buys if aid in top_20_buy2buy]))
    cart_order_num_counter  = Counter(aids2)
    buy_buy_num_counter = Counter(aids3)
    # RERANK CANDIDATES
    top_aids2 = [aid2 for aid2, cnt in Counter(aids2 + aids3).most_common(rec_num) if aid2 not in unique_aids]

    # get the candidate
    result = unique_aids + top_aids2[:rec_num - len(unique_aids)]
    # USE TOP20 TEST ORDERS
    final_aid_lst = result + list(top_orders)[:rec_num - len(result)]

    type_weight_current_session = [type_weight_dict.get(aid, 0) for aid in final_aid_lst]
    card_order_num = [cart_order_num_counter.get(aid, 0) for aid in final_aid_lst]
    buy_buy_num = [buy_buy_num_counter.get(aid, 0) for aid in final_aid_lst]

    #     # += [0] * (rec_num - len(type_weight_current_session))
    # if sum(type_weight_current_session) > 0:
    #     print(type_weight_current_session)
    # assert len(final_aid_lst) == len(
    #     type_weight_current_session), f"{len(final_aid_lst)} VS {len(type_weight_current_session)}"

    return final_aid_lst, type_weight_current_session, card_order_num, buy_buy_num