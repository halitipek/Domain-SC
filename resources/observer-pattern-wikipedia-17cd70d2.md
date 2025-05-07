# Observer pattern - Wikipedia

Source: https://en.wikipedia.org/wiki/Observer_pattern

## Identified Architecture Patterns

### Event Driven

- It is often used for implementing distributed [event-handling](/wiki/Event_handling "Event handling") systems in [event-driven software](/wiki/Event-driven_programming "Event-driven programming").
- Other implementations of the publish-subscribe pattern, which achieve a similar effect of notification and communication to interested parties, do not use the observer pattern.[[3]](#cite_note-3)[[4]](#cite_note-4)

In early implementations of multi-window operating systems such as [OS/2](/wiki/OS/2 "OS/2") and [Windows](/wiki/Microsoft_Windows "Microsoft Windows"), the terms "publish-subscribe pattern" and "event-driven software development" were used as synonyms for the observer pattern.[[5]](#cite_note-5)

The observer pattern, as described in the *Design Patterns* book, is a very basic concept and does not address removing interest in changes to the observed subject or special logic to be performed by the observed subject before or after notifying the observers.
- In some ([non-polling](/wiki/Polling_(computer_science) "Polling (computer science)")) implementations of the [publish-subscribe pattern](/wiki/Publish-subscribe_pattern "Publish-subscribe pattern"), this is solved by creating a dedicated message queue server (and sometimes an extra message handler object) as an extra stage between the observer and the object being observed, thus decoupling the components.

### Creational Patterns

- Related patterns include publish–subscribe, [mediator](/wiki/Mediator_pattern "Mediator pattern") and [singleton](/wiki/Singleton_pattern "Singleton pattern").

### Behavioral Patterns

- # Observer pattern - Wikipedia

Source: https://en.wikipedia.org/wiki/Observer_pattern

From Wikipedia, the free encyclopedia

Software design pattern based on an event-updated object with a list of dependents

In [software design](/wiki/Software_design "Software design") and [engineering](/wiki/Software_engineering "Software engineering"), the **observer pattern** is a [software design pattern](/wiki/Software_design_pattern "Software design pattern") in which an [object](/wiki/Object_(computer_science)#Objects_in_object-oriented_programming "Object (computer science)"), named the ***subject***, maintains a list of its dependents, called ***observers***, and notifies them automatically of any [state changes](/wiki/Event_(computing) "Event (computing)"), usually by calling one of their [methods](/wiki/Method_(computer_science) "Method (computer science)").
- Overview
--------

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=1 "Edit section: Overview")]

The observer design pattern is a behavioural pattern listed among the 23 well-known ["Gang of Four" design patterns](/wiki/Design_Patterns "Design Patterns") that address recurring design challenges in order to design flexible and reusable object-oriented software, yielding objects that are easier to implement, change, test and reuse.[[1]](#cite_note-GoF-1)

The observer pattern addresses the following problems:[[2]](#cite_note-2)

* A one-to-many dependency between objects should be defined without making the objects tightly coupled.
- weak reference")]

The observer pattern can cause [memory leaks](/wiki/Memory_leak "Memory leak"), known as the [lapsed listener problem](/wiki/Lapsed_listener_problem "Lapsed listener problem"), because in a basic implementation, it requires both explicit registration and explicit deregistration, as in the [dispose pattern](/wiki/Dispose_pattern "Dispose pattern"), because the subject holds strong references to the observers, keeping them alive.

### Data Storage

- However, it might be applicable from a performance point of view or if the object implementation is tightly coupled (such as low-level kernel structures that execute thousands of times per second).
- Other implementations of the publish-subscribe pattern, which achieve a similar effect of notification and communication to interested parties, do not use the observer pattern.[[3]](#cite_note-3)[[4]](#cite_note-4)

In early implementations of multi-window operating systems such as [OS/2](/wiki/OS/2 "OS/2") and [Windows](/wiki/Microsoft_Windows "Microsoft Windows"), the terms "publish-subscribe pattern" and "event-driven software development" were used as synonyms for the observer pattern.[[5]](#cite_note-5)

The observer pattern, as described in the *Design Patterns* book, is a very basic concept and does not address removing interest in changes to the observed subject or special logic to be performed by the observed subject before or after notifying the observers.
- When a string is supplied from `System.in`, the method `notifyObservers()` is then called in order to notify all observers of the event's occurrence, in the form of an invocation of their update methods.

### Api Design

- Other implementations of the publish-subscribe pattern, which achieve a similar effect of notification and communication to interested parties, do not use the observer pattern.[[3]](#cite_note-3)[[4]](#cite_note-4)

In early implementations of multi-window operating systems such as [OS/2](/wiki/OS/2 "OS/2") and [Windows](/wiki/Microsoft_Windows "Microsoft Windows"), the terms "publish-subscribe pattern" and "event-driven software development" were used as synonyms for the observer pattern.[[5]](#cite_note-5)

The observer pattern, as described in the *Design Patterns* book, is a very basic concept and does not address removing interest in changes to the observed subject or special logic to be performed by the observed subject before or after notifying the observers.


---

From Wikipedia, the free encyclopedia

Software design pattern based on an event-updated object with a list of dependents

In [software design](/wiki/Software_design "Software design") and [engineering](/wiki/Software_engineering "Software engineering"), the **observer pattern** is a [software design pattern](/wiki/Software_design_pattern "Software design pattern") in which an [object](/wiki/Object_(computer_science)#Objects_in_object-oriented_programming "Object (computer science)"), named the ***subject***, maintains a list of its dependents, called ***observers***, and notifies them automatically of any [state changes](/wiki/Event_(computing) "Event (computing)"), usually by calling one of their [methods](/wiki/Method_(computer_science) "Method (computer science)").

It is often used for implementing distributed [event-handling](/wiki/Event_handling "Event handling") systems in [event-driven software](/wiki/Event-driven_programming "Event-driven programming"). In such systems, the subject is usually named a "stream of events" or "stream source of events" while the observers are called "sinks of events." The stream nomenclature alludes to a physical setup in which the observers are physically separated and have no control over the emitted events from the subject/stream source. This pattern thus suits any process by which data arrives from some input that is not available to the [CPU](/wiki/CPU "CPU") at [startup](/wiki/Booting "Booting"), but instead may arrive at arbitrary or indeterminate times ([HTTP requests](/wiki/HTTP_request "HTTP request"), [GPIO](/wiki/GPIO "GPIO") data, [user input](/wiki/User_input "User input") from [peripherals](/wiki/Peripheral "Peripheral") and [distributed databases](/wiki/Distributed_database "Distributed database"), etc.).

Overview
--------

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=1 "Edit section: Overview")]

The observer design pattern is a behavioural pattern listed among the 23 well-known ["Gang of Four" design patterns](/wiki/Design_Patterns "Design Patterns") that address recurring design challenges in order to design flexible and reusable object-oriented software, yielding objects that are easier to implement, change, test and reuse.[[1]](#cite_note-GoF-1)

The observer pattern addresses the following problems:[[2]](#cite_note-2)

* A one-to-many dependency between objects should be defined without making the objects tightly coupled.
* When one object changes state, an open-ended number of dependent objects should be updated automatically.
* An object can notify multiple other objects.

Defining a one-to-many dependency between objects by defining one object (subject) that updates the state of dependent objects directly is inflexible because it couples the subject to particular dependent objects. However, it might be applicable from a performance point of view or if the object implementation is tightly coupled (such as low-level kernel structures that execute thousands of times per second). Tightly coupled objects can be difficult to implement in some scenarios and are not easily reused because they refer to and are aware of many objects with different interfaces. In other scenarios, tightly coupled objects can be a better option because the compiler is able to detect errors at compile time and optimize the code at the CPU instruction level.

* Define `Subject` and `Observer` objects.
* When a subject changes state, all registered observers are notified and updated automatically (and probably asynchronously).

The sole responsibility of a subject is to maintain a list of observers and to notify them of state changes by calling their `update()` operation. The responsibility of observers is to register and unregister themselves with a subject (in order to be notified of state changes) and to update their state (to synchronize their state with the subject's state) when they are notified. This makes subject and observers loosely coupled. Subject and observers have no explicit knowledge of each other. Observers can be added and removed independently at run time. This notification-registration interaction is also known as [publish-subscribe](/wiki/Publish-subscribe "Publish-subscribe").

Strong vs. weak reference
-------------------------

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=2 "Edit section: Strong vs. weak reference")]

The observer pattern can cause [memory leaks](/wiki/Memory_leak "Memory leak"), known as the [lapsed listener problem](/wiki/Lapsed_listener_problem "Lapsed listener problem"), because in a basic implementation, it requires both explicit registration and explicit deregistration, as in the [dispose pattern](/wiki/Dispose_pattern "Dispose pattern"), because the subject holds strong references to the observers, keeping them alive. This can be prevented if the subject holds [weak references](/wiki/Weak_reference "Weak reference") to the observers.

Coupling and typical publish-subscribe implementations
------------------------------------------------------

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=3 "Edit section: Coupling and typical publish-subscribe implementations")]

Typically, the observer pattern is implemented so that the subject being observed is part of the object for which state changes are being observed (and communicated to the observers). This type of implementation is considered [tightly coupled](/wiki/Coupling_(computer_programming) "Coupling (computer programming)"), forcing both the observers and the subject to be aware of each other and have access to their internal parts, creating possible issues of [scalability](/wiki/Scalability "Scalability"), speed, message recovery and maintenance (also called event or notification loss), the lack of flexibility in conditional dispersion and possible hindrance to desired security measures. In some ([non-polling](/wiki/Polling_(computer_science) "Polling (computer science)")) implementations of the [publish-subscribe pattern](/wiki/Publish-subscribe_pattern "Publish-subscribe pattern"), this is solved by creating a dedicated message queue server (and sometimes an extra message handler object) as an extra stage between the observer and the object being observed, thus decoupling the components. In these cases, the message queue server is accessed by the observers with the observer pattern, subscribing to certain messages and knowing (or not knowing, in some cases) about only the expected message, while knowing nothing about the message sender itself; the sender may also know nothing about the observers. Other implementations of the publish-subscribe pattern, which achieve a similar effect of notification and communication to interested parties, do not use the observer pattern.[[3]](#cite_note-3)[[4]](#cite_note-4)

In early implementations of multi-window operating systems such as [OS/2](/wiki/OS/2 "OS/2") and [Windows](/wiki/Microsoft_Windows "Microsoft Windows"), the terms "publish-subscribe pattern" and "event-driven software development" were used as synonyms for the observer pattern.[[5]](#cite_note-5)

The observer pattern, as described in the *Design Patterns* book, is a very basic concept and does not address removing interest in changes to the observed subject or special logic to be performed by the observed subject before or after notifying the observers. The pattern also does not deal with recording change notifications or guaranteeing that they are received. These concerns are typically handled in message-queueing systems, in which the observer pattern plays only a small part.

Related patterns include publish–subscribe, [mediator](/wiki/Mediator_pattern "Mediator pattern") and [singleton](/wiki/Singleton_pattern "Singleton pattern").

### Uncoupled

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=4 "Edit section: Uncoupled")]

The observer pattern may be used in the absence of publish-subscribe, as when model status is frequently updated. Frequent updates may cause the view to become unresponsive (e.g., by invoking many [repaint](/wiki/Painter%27s_algorithm "Painter's algorithm") calls); such observers should instead use a timer. Instead of becoming overloaded by change message, the observer will cause the view to represent the approximate state of the model at a regular interval. This mode of observer is particularly useful for [progress bars](/wiki/Progress_bar "Progress bar"), in which the underlying operation's progress changes frequently.

Structure
---------

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=5 "Edit section: Structure")]

### UML class and sequence diagram

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=6 "Edit section: UML class and sequence diagram")]

[![](//upload.wikimedia.org/wikipedia/commons/0/01/W3sDesign_Observer_Design_Pattern_UML.jpg)](/wiki/File:W3sDesign_Observer_Design_Pattern_UML.jpg)

A sample UML class and sequence diagram for the observer design pattern. [[6]](#cite_note-6)

In this [UML](/wiki/Unified_Modeling_Language "Unified Modeling Language") [class diagram](/wiki/Class_diagram "Class diagram"), the `Subject` class does not update the state of dependent objects directly. Instead, `Subject` refers to the `Observer` interface (`update()`) for updating state, which makes the `Subject` independent of how the state of dependent objects is updated. The `Observer1` and `Observer2` classes implement the `Observer` interface by synchronizing their state with subject's state.

The [UML](/wiki/Unified_Modeling_Language "Unified Modeling Language") [sequence diagram](/wiki/Sequence_diagram "Sequence diagram") shows the runtime interactions: The `Observer1` and `Observer2` objects call `attach(this)` on `Subject1` to register themselves. Assuming that the state of `Subject1` changes, `Subject1` calls `notify()` on itself. `notify()` calls `update()` on the registered `Observer1` and `Observer2`objects, which request the changed data (`getState()`) from `Subject1` to update (synchronize) their state.

### UML class diagram

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=7 "Edit section: UML class diagram")]

[![](//upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Observer_w_update.svg/500px-Observer_w_update.svg.png)](/wiki/File:Observer_w_update.svg)

[UML](/wiki/Unified_Modeling_Language "Unified Modeling Language") class diagram of Observer pattern

Example
-------

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=8 "Edit section: Example")]

While the library classes [`java.util.Observer`](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/Observer.html) and [`java.util.Observable`](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/Observable.html) exist, they have been [deprecated](/wiki/Deprecation "Deprecation") in Java 9 because the model implemented was quite limited.

Below is an example written in [Java](/wiki/Java_(programming_language) "Java (programming language)") that takes keyboard input and handles each input line as an event. When a string is supplied from `System.in`, the method `notifyObservers()` is then called in order to notify all observers of the event's occurrence, in the form of an invocation of their update methods.

### Java

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=9 "Edit section: Java")]

```
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

interface Observer {
    void update(String event);
}
  
class EventSource {
    List<Observer> observers = new ArrayList<>();
  
    public void notifyObservers(String event) {
        observers.forEach(observer -> observer.update(event));
    }
  
    public void addObserver(Observer observer) {
        observers.add(observer);
    }
  
    public void scanSystemIn() {
        Scanner scanner = new Scanner(System.in);
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            notifyObservers(line);
        }
    }
}

public class ObserverDemo {
    public static void main(String[] args) {
        System.out.println("Enter Text: ");
        EventSource eventSource = new EventSource();
        
        eventSource.addObserver(event -> System.out.println("Received response: " + event));

        eventSource.scanSystemIn();
    }
}

```

### C++

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=10 "Edit section: C++")]

This is a C++11 implementation.

```
#include <functional>
#include <iostream>
#include <list>

class Subject; //Forward declaration for usage in Observer

class Observer
{
public:
    explicit Observer(Subject& subj);
    virtual ~Observer();
  
    Observer(const Observer&) = delete; // rule of three
    Observer& operator=(const Observer&) = delete;

    virtual void update( Subject& s) const = 0;
private:
    // Reference to a Subject object to detach in the destructor
    Subject& subject;
};

// Subject is the base class for event generation
class Subject
{
public:
    using RefObserver = std::reference_wrapper<const Observer>;
  
    // Notify all the attached observers
    void notify()
    {
        for (const auto& x: observers) 
        {
            x.get().update(*this);
        }
    }
  
    // Add an observer
    void attach(const Observer& observer) 
    {
        observers.push_front(observer);
    }
  
    // Remove an observer
    void detach(Observer& observer)
    {
        observers.remove_if( [&observer ](const RefObserver& obj)
        { 
            return &obj.get()==&observer; 
        });
    }
  
private:
    std::list<RefObserver> observers;
};

Observer::Observer(Subject& subj) : subject(subj)
{
    subject.attach(*this);
}

Observer::~Observer()
{
    subject.detach(*this);
}


// Example of usage
class ConcreteObserver: public Observer
{
public:
    ConcreteObserver(Subject& subj) : Observer(subj) {}
  
    // Get notification
    void update(Subject&) const override
    {
        std::cout << "Got a notification" << std::endl;
    }
};

int main() 
{
    Subject cs;
    ConcreteObserver co1(cs);
    ConcreteObserver co2(cs);
    cs.notify();
}

```

The program output is like

```
Got a notification
Got a notification

```

### Groovy

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=11 "Edit section: Groovy")]

```
class EventSource {
    private observers = []

    private notifyObservers(String event) {
        observers.each { it(event) }
    }

    void addObserver(observer) {
        observers += observer
    }

    void scanSystemIn() {
        var scanner = new Scanner(System.in)
        while (scanner) {
            var line = scanner.nextLine()
            notifyObservers(line)
        }
    }
}

println 'Enter Text: '
var eventSource = new EventSource()

eventSource.addObserver { event ->
    println "Received response: $event"
}

eventSource.scanSystemIn()

```

### Kotlin

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=12 "Edit section: Kotlin")]

```
import java.util.Scanner

typealias Observer = (event: String) -> Unit;

class EventSource {
    private var observers = mutableListOf<Observer>()

    private fun notifyObservers(event: String) {
        observers.forEach { it(event) }
    }

    fun addObserver(observer: Observer) {
        observers += observer
    }

    fun scanSystemIn() {
        val scanner = Scanner(System.`in`)
        while (scanner.hasNext()) {
            val line = scanner.nextLine()
            notifyObservers(line)
        }
    }
}

```

```
fun main(arg: List<String>) {
    println("Enter Text: ")
    val eventSource = EventSource()

    eventSource.addObserver { event ->
        println("Received response: $event")
    }

    eventSource.scanSystemIn()
}

```

### Delphi

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=13 "Edit section: Delphi")]

```
uses
  System.Generics.Collections, System.SysUtils;

type
  IObserver = interface
    ['{0C8F4C5D-1898-4F24-91DA-63F1DD66A692}']
    procedure Update(const AValue: string);
  end;

type
  TObserverManager = class
  private
    FObservers: TList<IObserver>;
  public
    constructor Create; overload;
    destructor Destroy; override;
    procedure NotifyObservers(const AValue: string);
    procedure AddObserver(const AObserver: IObserver);
    procedure UnregisterObsrver(const AObserver: IObserver);
  end;

type
  TListener = class(TInterfacedObject, IObserver)
  private
    FName: string;
  public
    constructor Create(const AName: string); reintroduce;
    procedure Update(const AValue: string);
  end;

procedure TObserverManager.AddObserver(const AObserver: IObserver);
begin
  if not FObservers.Contains(AObserver)
    then FObservers.Add(AObserver);
end;

begin
  FreeAndNil(FObservers);
  inherited;
end;

procedure TObserverManager.NotifyObservers(const AValue: string);
var
  i: Integer;
begin
  for i := 0 to FObservers.Count - 1 do
    FObservers[i].Update(AValue);
end;

procedure TObserverManager.UnregisterObsrver(const AObserver: IObserver);
begin
  if FObservers.Contains(AObserver)
    then FObservers.Remove(AObserver);
end;

constructor TListener.Create(const AName: string);
begin
  inherited Create;
  FName := AName;
end;

procedure TListener.Update(const AValue: string);
begin
  WriteLn(FName + ' listener received notification: ' + AValue);
end;

procedure TMyForm.ObserverExampleButtonClick(Sender: TObject);
var
  LDoorNotify: TObserverManager;
  LListenerHusband: IObserver;
  LListenerWife: IObserver;
begin
  LDoorNotify := TObserverManager.Create;
  try
    LListenerHusband := TListener.Create('Husband');
    LDoorNotify.AddObserver(LListenerHusband);
    LListenerWife := TListener.Create('Wife');
    LDoorNotify.AddObserver(LListenerWife);
    LDoorNotify.NotifyObservers('Someone is knocking on the door');
  finally
    FreeAndNil(LDoorNotify);
  end;
end;

```

Output

```
Husband listener received notification: Someone is knocking on the door
Wife listener received notification: Someone is knocking on the door

```

### Python

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=14 "Edit section: Python")]

A similar example in [Python](/wiki/Python_(programming_language) "Python (programming language)"):

```
class Observable:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer) -> None:
        self._observers.append(observer)

    def notify_observers(self, *args, **kwargs) -> None:
        for observer in self._observers:
            observer.notify(self, *args, **kwargs)


class Observer:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self, observable, *args, **kwargs) -> None:
        print("Got", args, kwargs, "From", observable)


subject = Observable()
observer = Observer(subject)
subject.notify_observers("test", kw="python")

# prints: Got ('test',) {'kw': 'python'} From <__main__.Observable object at 0x0000019757826FD0>

```

### C#

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=15 "Edit section: C#")]

C# provides the `IObservable`.[[7]](#cite_note-7) and `IObserver`[[8]](#cite_note-8) interfaces as well as documentation on how to implement the design pattern.[[9]](#cite_note-9)

```
class Payload
{
    internal string Message { get; set; }
}

class Subject : IObservable<Payload>
{
    private readonly ICollection<IObserver<Payload>> _observers = new List<IObserver<Payload>>();

    IDisposable IObservable<Payload>.Subscribe(IObserver<Payload> observer)
    {         
        if (!_observers.Contains(observer))
        {
            _observers.Add(observer);
        }

        return new Unsubscriber(observer, _observers);
    }

    internal void SendMessage(string message)
    {
        foreach (var observer in _observers)
        {
            observer.OnNext(new Payload { Message = message });
        }
    }
}

internal class Unsubscriber : IDisposable
{
    private readonly IObserver<Payload> _observer;
    private readonly ICollection<IObserver<Payload>> _observers;

    internal Unsubscriber(
        IObserver<Payload> observer,
        ICollection<IObserver<Payload>> observers)
    {
        _observer = observer;
        _observers = observers;
    }

    void IDisposable.Dispose()
    {
        if (_observer != null && _observers.Contains(_observer))
        {
            _observers.Remove(_observer);
        }
    }
}

internal class Observer : IObserver<Payload>
{
    internal string Message { get; set; }

    public void OnCompleted()
    {
    }

    public void OnError(Exception error)
    {
    }

    public void OnNext(Payload value)
    {
        Message = value.Message;
    }

    internal IDisposable Register(IObservable<Payload> subject)
    {
        return subject.Subscribe(this);
    }
}

```

### JavaScript

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=16 "Edit section: JavaScript")]

JavaScript has a deprecated `Object.observe` function that was a more accurate implementation of the observer pattern.[[10]](#cite_note-10) This would fire events upon change to the observed object. Without the deprecated `Object.observe` function, the pattern may be implemented with more explicit code:[[11]](#cite_note-11)

```
let Subject = {
    _state: 0,
    _observers: [],
    add: function(observer) {
        this._observers.push(observer);
    },
    getState: function() {
        return this._state;
    },
    setState: function(value) {
        this._state = value;
        for (let i = 0; i < this._observers.length; i++)
        {
            this._observers[i].signal(this);
        }
    }
};

let Observer = {
    signal: function(subject) {
        let currentValue = subject.getState();
        console.log(currentValue);
    }
}

Subject.add(Observer);
Subject.setState(10);
//Output in console.log - 10

```

See also
--------

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=17 "Edit section: See also")]

* [Implicit invocation](/wiki/Implicit_invocation "Implicit invocation")
* [Client–server model](/wiki/Client%E2%80%93server_model "Client–server model")
* The observer pattern is often used in the [entity–component–system](/wiki/Entity%E2%80%93component%E2%80%93system "Entity–component–system") pattern

References
----------

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=18 "Edit section: References")]

1. **[^](#cite_ref-GoF_1-0)** Erich Gamma; Richard Helm; Ralph Johnson; John Vlissides (1994). [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://archive.org/details/designpatternsel00gamm/page/293). Addison Wesley. pp. [293ff](https://archive.org/details/designpatternsel00gamm/page/293). [ISBN](/wiki/ISBN_(identifier) "ISBN (identifier)") [0-201-63361-2](/wiki/Special:BookSources/0-201-63361-2 "Special:BookSources/0-201-63361-2").
2. **[^](#cite_ref-2)** ["Observer Design Pattern"](https://www.geeksforgeeks.org/observer-pattern-set-1-introduction/). *www.geeksforgeeks.org*.
3. **[^](#cite_ref-3)** [Comparison between different observer pattern implementations](https://github.com/millermedeiros/js-signals/wiki/Comparison-between-different-Observer-Pattern-implementations) Moshe Bindler, 2015 (Github)
4. **[^](#cite_ref-4)** [Differences between pub/sub and observer pattern](https://www.safaribooksonline.com/library/view/learning-javascript-design/9781449334840/ch09s05.html) The Observer Pattern by Adi Osmani (Safari books online)
5. **[^](#cite_ref-5)** [The Windows Programming Experience](https://books.google.com/books?id=18wFKrkDdM0C&pg=PA230&lpg=PA230) [Charles Petzold](/wiki/Charles_Petzold "Charles Petzold"), Nov 10, 1992, [PC Magazine](/wiki/PC_Magazine "PC Magazine") ([Google Books](/wiki/Google_Books "Google Books"))
6. **[^](#cite_ref-6)** ["The Observer design pattern - Structure and Collaboration"](http://w3sdesign.com/?gr=b07&ugr=struct). *w3sDesign.com*. Retrieved 2017-08-12.
7. **[^](#cite_ref-7)** ["IObservable Interface (System)"](https://learn.microsoft.com/en-us/dotnet/api/system.iobservable-1?view=net-8.0). *learn.microsoft.com*. Retrieved 9 November 2024.
8. **[^](#cite_ref-8)** ["IObserver Interface (System)"](https://learn.microsoft.com/en-us/dotnet/api/system.iobserver-1?view=net-8.0). *learn.microsoft.com*. Retrieved 9 November 2024.
9. **[^](#cite_ref-9)** ["Observer design pattern - .NET"](https://learn.microsoft.com/en-us/dotnet/standard/events/observer-design-pattern). *learn.microsoft.com*. 25 May 2023. Retrieved 9 November 2024.
10. **[^](#cite_ref-10)** ["jQuery - Listening for variable changes in JavaScript"](https://stackoverflow.com/a/50862441/887092).
11. **[^](#cite_ref-11)** ["Jquery - Listening for variable changes in JavaScript"](https://stackoverflow.com/a/37403125/887092).

External links
--------------

[[edit](/w/index.php?title=Observer_pattern&action=edit&section=19 "Edit section: External links")]

* [![](//upload.wikimedia.org/wikipedia/commons/thumb/d/df/Wikibooks-logo-en-noslogan.svg/20px-Wikibooks-logo-en-noslogan.svg.png)](/wiki/File:Wikibooks-logo-en-noslogan.svg) [Observer implementations in various languages](https://en.wikibooks.org/wiki/Computer_Science_Design_Patterns/Observer "wikibooks:Computer Science Design Patterns/Observer") at Wikibooks

![](https://en.wikipedia.org/wiki/Special:CentralAutoLogin/start?type=1x1&usesul3=1)

Retrieved from "<https://en.wikipedia.org/w/index.php?title=Observer_pattern&oldid=1272189362>"

[Category](/wiki/Help:Category "Help:Category"):

* [Software design patterns](/wiki/Category:Software_design_patterns "Category:Software design patterns")

Hidden categories:

* [Articles with short description](/wiki/Category:Articles_with_short_description "Category:Articles with short description")
* [Short description is different from Wikidata](/wiki/Category:Short_description_is_different_from_Wikidata "Category:Short description is different from Wikidata")
* [Articles with example Java code](/wiki/Category:Articles_with_example_Java_code "Category:Articles with example Java code")
* [Articles with example Python (programming language) code](/wiki/Category:Articles_with_example_Python_(programming_language)_code "Category:Articles with example Python (programming language) code")
* [Articles with example C Sharp code](/wiki/Category:Articles_with_example_C_Sharp_code "Category:Articles with example C Sharp code")