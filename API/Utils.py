def clearWord(word):
    if "\n" in word:
        word.replace('\n', '')
    # if ' ' in word:
    #     word.replace(' ', '')
    return word.strip()


def countStars(word):
    return word.count('★')
