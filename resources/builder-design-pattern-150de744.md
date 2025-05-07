# Builder Design Pattern

Source: https://sourcemaking.com/design_patterns/builder

## Identified Architecture Patterns

### Creational Patterns

- Abstract Factory, Builder, and Prototype can use Singleton in their implementations.
- Abstract Factory emphasizes a family of product objects (either simple or complex).
- Builder returns the product as a final step, but as far as the Abstract Factory is concerned, the product gets returned immediately.

### Data Storage

- The "director" invokes "builder" services as it interprets the external format.
- The client creates a Reader object and a Builder object, and registers the latter with the former.
- * 22 design patterns and 8 principles explained in depth
* 406 well-structured, easy to read, jargon-free pages
* 228 clear and helpful illustrations and diagrams
* An archive with code examples in 4 languages
* All devices supported: EPUB/MOBI/PDF formats

 [Learn more...](/design-patterns-ebook)

### Code examples

|  |  |  |
| --- | --- | --- |
| Java | [Builder in Java: Before and after](/design_patterns/builder/java/1) | [Builder in Java](/design_patterns/builder/java/2) |
| C++ | [Builder in C++](/design_patterns/builder/cpp/1) |
| PHP | [Builder in PHP](/design_patterns/builder/php/1) |
| Delphi | [Builder in Delphi](/design_patterns/builder/delphi) |
| Python | [Builder in Python](/design_patterns/builder/python/1) |

### Api Design

- This pattern is used by fast food restaurants to construct children's meals.
- This same process is used at competing restaurants.


---

/ [Design Patterns](/design_patterns)
/ [Creational patterns](/design_patterns/creational_patterns)

Builder Design Pattern
======================

### Intent

* Separate the construction of a complex object from its representation so that the same construction process can create different representations.
* Parse a complex representation, create one of several targets.

### Problem

An application needs to create the elements of a complex aggregate. The specification for the aggregate exists on secondary storage and one of many representations needs to be built in primary storage.

### Discussion

Separate the algorithm for interpreting (i.e. reading and parsing) a stored persistence mechanism (e.g. RTF files) from the algorithm for building and representing one of many target products (e.g. ASCII, TeX, text widget). The focus/distinction is on creating complex aggregates.

The "director" invokes "builder" services as it interprets the external format. The "builder" creates part of the complex object each time it is called and maintains all intermediate state. When the product is finished, the client retrieves the result from the "builder".

Affords finer control over the construction process. Unlike creational patterns that construct products in one shot, the Builder pattern constructs the product step by step under the control of the "director".

### Structure

The Reader encapsulates the parsing of the common input. The Builder hierarchy makes possible the polymorphic creation of many peculiar representations or targets.

![Scheme of Builder](/files/v2/content/patterns/Builder.png)

### Example

The Builder pattern separates the construction of a complex object from its representation so that the same construction process can create different representations. This pattern is used by fast food restaurants to construct children's meals. Children's meals typically consist of a main item, a side item, a drink, and a toy (e.g., a hamburger, fries, Coke, and toy dinosaur). Note that there can be variation in the content of the children's meal, but the construction process is the same. Whether a customer orders a hamburger, cheeseburger, or chicken, the process is the same. The employee at the counter directs the crew to assemble a main item, side item, and toy. These items are then placed in a bag. The drink is placed in a cup and remains outside of the bag. This same process is used at competing restaurants.

![Example of Builder](/files/v2/content/patterns/Builder_example1.png)

### Check list

1. Decide if a common input and many possible representations (or outputs) is the problem at hand.
2. Encapsulate the parsing of the common input in a Reader class.
3. Design a standard protocol for creating all possible output representations. Capture the steps of this protocol in a Builder interface.
4. Define a Builder derived class for each target representation.
5. The client creates a Reader object and a Builder object, and registers the latter with the former.
6. The client asks the Reader to "construct".
7. The client asks the Builder to return the result.

### Rules of thumb

* Sometimes creational patterns are complementary: Builder can use one of the other patterns to implement which components get built. Abstract Factory, Builder, and Prototype can use Singleton in their implementations.
* Builder focuses on constructing a complex object step by step. Abstract Factory emphasizes a family of product objects (either simple or complex). Builder returns the product as a final step, but as far as the Abstract Factory is concerned, the product gets returned immediately.
* Builder often builds a Composite.
* Often, designs start out using Factory Method (less complicated, more customizable, subclasses proliferate) and evolve toward Abstract Factory, Prototype, or Builder (more flexible, more complex) as the designer discovers where more flexibility is needed.

[![](/images/content-public/didp-cover-en.png?id=2e1103ea2edb33a8979eebb8e1ba73b6)](/design-patterns-ebook)

### Support our free website and own the eBook!

* 22 design patterns and 8 principles explained in depth
* 406 well-structured, easy to read, jargon-free pages
* 228 clear and helpful illustrations and diagrams
* An archive with code examples in 4 languages
* All devices supported: EPUB/MOBI/PDF formats

 [Learn more...](/design-patterns-ebook)

### Code examples

|  |  |  |
| --- | --- | --- |
| Java | [Builder in Java: Before and after](/design_patterns/builder/java/1) | [Builder in Java](/design_patterns/builder/java/2) |
| C++ | [Builder in C++](/design_patterns/builder/cpp/1) |
| PHP | [Builder in PHP](/design_patterns/builder/php/1) |
| Delphi | [Builder in Delphi](/design_patterns/builder/delphi) |
| Python | [Builder in Python](/design_patterns/builder/python/1) |