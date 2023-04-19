This branch presents an idea for the potential design of Aniparser v2. Unfortunately,
due to time constraints and limited resources, I am unable to implement it myself.
However, I hope this concept will be useful to someone. If you are interested in developing this idea
and want to make it work, I would be happy to assist you.

If you succeed in making it work, please let me know. I would be excited to use it, and in that case,
I am willing to offer you the `aniparse` Python package name on PyPI if you want it,
as well as some compensation for your efforts.

Now, let's dive into the idea:

## token.py

### Classes:

* TokenType:

This class is used to classify tokens, with minimal differences compared to the previous version.

- Token:
  This class holds the token information, including its content, type, category, and nesting level.
  The nesting level is used to determine the group the token belongs to. For example, if the token
  is in the first parenthesis (BD), the nesting level is 1. If the token is in the second parenthesis
  (AAC {5.1+2.0}), the nesting level is 2, and so on. This is helpful when determining the unknown token
  type. For instance, the values 5.1 and 2.0 on their own are unclear in meaning. However, if we look at their
  parent token, we see AAC, which is identified as an audio_term. Therefore, we can assume that 5.1 and 2.0
  represent audio channels. The Token class also has an attribute called "possibilities," which is a set of
  potential classifications the token can have.
- Tokens:
  This class holds the token list and includes tokens, lookup_category, and lookup_possibilities attributes.
  The primary reason for using a list here is that this class is designed for iterating through the list,
  which makes lists more efficient than doubly linked lists. The overhead of using a doubly linked list is not
  justified since we expect to perform more iterations than insertions or deletions of tokens.
  Additionally, creating loops with doubly linked lists is not as straightforward as it may seem. For example,
  when wanting to loop through tokens from 'current' to 'stop_token':

  ```python
  while current is not stop_token and current is not None:
        yield current
  current = current.next
  ```

  In this example, if 'current' is the same as 'stop_token', nothing will be yielded. Conversely, if 'stop_token'
  is not the same as 'current', the loop will still yield the 'current' token before iterating. Moreover, while
  loops are generally slower than for loops in Python. Therefore, using a list is the preferred choice.
- While this class is mostly finish, you can use it as is.

## tokenizer.py

Classes:

- Tokenizer:
  The Tokenizer class is responsible for tokenizing the input string. Its implementation is similar to the previous version.
  First, it checks for brackets and balances them if possible. Then, it splits the string into tokens based on brackets
  and delimiters. Finally, it populates the Tokens class with the tokens.

  This class is mostly complete and can be used as is. However, there is a concern regarding the following lines of code:

  ```python
  if (sub_text in self.options.allowed_delimiter and
      # This character is not part of range_separator
      sub_text not in constant.RANGE_SEPARATOR):
  ```

  The issue arises because tokens are split by user-defined delimiters, and if a delimiter is also a range separator,
  we want to retain it as a token. Examples include '&' and the dash symbol ('-'). we could implement validate_delimiter
  after splitting like we did in the previous version, but the choice is up to you.

## element.py

Classes:

* ElementCategory:
  * The ElementCategory class is used to classify elements, with only minimal differences compared to the previous version.

- Element:
  - BATCH: This is used to identify the batch element, such as season 1, 2, movies, arc titles, etc.
  - CONTEXT_DELIMITER: This is used to identify the context delimiter, like dashes used as separators between contexts.
  - CREDIT_NUMBER: This is used to identify opening and ending numbers without interfering with episode numbers.
  - DELIMITER_IN_GROUP: This is used to identify delimiters within groups, such as anime titles, episode titles, etc.
  - SUBTITLE_TYPE: It is suggested to separate soft subs and hard subs into the subtitle type category, while the rest remains in SUBTITLES.
  - SUBTITLES: I want to change this category to SUBTITLE_TERM in order to maintain consistency with audio and video categories.

## keyword.py

Classes:

* KeywordOption:
  * This class holds the options for each keyword, such as whether it's searchable, identifiable, or valid. These metrics are used to determine
    if a token can be identified as a keyword during pre-processing, validation with surrounding tokens, or only during post-processing.
* Keyword:
  * This class holds the keyword information, such as the category and options. I plan to add invalid_prefix and invalid_suffix attributes to this class
    to help with validation. For example, if the keyword is 'END', the invalid_prefix would be 'the'. In general, the token "the" is mostly incompatible
    with any keyword. However, I am not sure how to make this feature work yet.
* KeywordManager:
  * This class is responsible for managing the keywords. It is used to load the keywords from a JSON file and to validate the keywords.
  * This class is mostly complete, except for the invalid_prefix and invalid_suffix attributes. It also handles cases when the keyword has a delimiter in it.
    One idea I want to add here is to include observers so that if the `options` change, the `keyword` will be updated as well.
  * Lastly, the ability to export as a JSON file should be added. This should not be difficult, as I've done it before in the [dev-experiment](https://github.com/MeGaNeKoS/Aniparse/tree/dev-experiment) branch.

## constant.py

As the name suggests, this file contains constants. Some of them could be moved in the future. For example the `ORDINALS`, `RANGE_TOTAL`, etc could be moved into `parser_options`instead.

## parser_options.py

This class is replacement for old default_option dict. By using a class, we can get benefit from type hinting and IDE auto-completion. Moreover, we can add
additional methods to this class to make it easier to use and maintain. This is still rough idea but I think it's better than the old dict.

## parser.py

This class have been rework again. I'm thinking to use a BaseParser for constructor, and inherit it to ParserNumber and ParserUtil. ParserNumber will be used for make logic related to episode number and volume number. And ParserUtil basically the old parser_helper.py.

# Rules Documentation

In this project, we use a `rules` folder, where each element has its own corresponding text file. These text files serve as documentation for the rules associated with each element, detailing the conditions under which the element is considered valid, and where in the code this validation is implemented.

This approach ensures that the rules for each element are clearly documented and organized, making it easier for developers to understand and modify the validation logic as needed.

# Parser Method

The following steps outline the method used for parsing the filename:

1. Tokenize the filename: Break the filename into individual tokens for easier processing.
2. Pre-processing: Populate the possibilities for each token based on pre-defined rules and patterns.
3. Validation: Validate each token and its possibilities to ensure accuracy.
4. Episode number identification: Identify the episode number, ensuring that it is not confused with anime year or screen resolution values.
5. Locate title, episode title, and release group information.
6. Perform any necessary intermediate actions, such as additional validation or reordering of tokens.
7. Post-processing: Finalize the output by applying any required modifications, such as formatting or additional data extraction.
8. Build the cleaned output dictionary containing the parsed information, ready for further use or storage.

# Output

In the new version of the parser, there will be three different output formats to cater to various use cases:

1. Original output: This output format will be the same as in the previous version, providing the parsed information with enum values.
2. Enum-based output: Instead of using enum values, this output format will use the enums themselves. This can be helpful for better understanding and readability.
3. Tokenized and parsed output: This output format will provide the tokenized and parsed tokens, allowing for greater flexibility in post-processing. Users can further process the output to convert it to their preferred format. For example, they can change the 'audio_term' in the output to 'audio_lang' to better suit their needs.

By offering multiple output formats, the new version of the parser will be more versatile and useful for a wider range of users.

# IDEA

A custom regex builder could be a powerful addition to the parser. It would allow for easy creation and modification of patterns for various elements without having to modify the code directly. Users could quickly add new patterns as needed, making the parser more adaptable and versatile. 

One significant advantage of this approach is the ability to keep track of the categories associated with each group in the pattern. This can help streamline the parsing process and improve accuracy.

An example implementation can be found in `idea/parser_number.py` and `tests/test_parser_number.py`. This demonstration illustrates how a custom regex builder can be used to validate multi-season-episode-patterns.

Overall, a custom regex builder would offer a more flexible and user-friendly solution for defining and managing patterns in the parser.

# Notes

Although the master branch already produces the expected results, the workarounds implemented to achieve it make the code quite messy. Since I don't have much time to focus on this project and the goals have already been achieved, I don't think I will return to this project in a year or so, unless there are bugs or changes needed in the master branch.

# End Notes

If you need more information or assistance, please feel free to contact me. I will be happy to help. You can reach me at [Taiga server](https://github.com/erengy/taiga) or [Reddit](https://www.reddit.com/user/MeGaNeKoS).

Lastly, I am considering changing the project license if this version goes well. I am thinking of using GNU GPL v3, as it is more flexible and compatible with other licenses while preserving intellectual property rights. However, this decision will depend on how much we change the original [anitomy](https://github.com/erengy/anitomy). It is essential to consult with the original author first before making any changes to the license.

