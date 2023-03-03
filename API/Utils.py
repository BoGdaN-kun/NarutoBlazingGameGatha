def clearWord(word):
    if "\n" in word:
        word.replace('\n', '')
    # if ' ' in word:
    #     word.replace(' ', '')
    return word


def countStars(word):
    return word.count('★')
