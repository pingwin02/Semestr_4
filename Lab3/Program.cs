using System.Data;
using System.Xml;
using System.Xml.Linq;
using System.Xml.Serialization;
using System.Xml.XPath;

namespace Lab3
{
    internal class Program
    {
        static List<Car> myCars = new(){
            new Car("E250", new Engine(1.8, 204, "CGI"), 2009),
            new Car("E350", new Engine(3.5, 292, "CGI"), 2009),
            new Car("A6", new Engine(2.5, 187, "FSI"), 2012),
            new Car("A6", new Engine(2.8, 220, "FSI"), 2012),
            new Car("A6", new Engine(3.0, 295, "TFSI"), 2012),
            new Car("A6", new Engine(2.0, 175, "TDI"), 2011),
            new Car("A6", new Engine(3.0, 309, "TDI"), 2011),
            new Car("S6", new Engine(4.0, 414, "TFSI"), 2012),
            new Car("S8", new Engine(4.0, 513, "TFSI"), 2012)
        };
        static void Main()
        {
            Console.WriteLine("Exercise 1:\n");
            Exercise1();
            Console.WriteLine("\nExercise 2:\n");
            Exercise2();
            Console.WriteLine("\nExercise 3:\n");
            Exercise3();
            Console.WriteLine("\nExercise 4:\n");
            Exercise4();
            Console.WriteLine("\nExercise 5:\n");
            Exercise5();
            Console.WriteLine("\nExercise 6:\n");
            Exercise6();
        }

        private static void Exercise1()
        {
            var result = from car in myCars
                         where car.model == "A6"
                         select new
                         {
                             engineType = car.engine.model.Contains("TDI") ? "diesel" : "petrol",
                             hppl = car.engine.horsePower / car.engine.displacement
                         };

            foreach (var item in result)
            {
                Console.WriteLine(item);
            }

            foreach (var item in result.GroupBy(x => x.engineType))
            {
                Console.WriteLine($"{item.Key} : {item.Average(x => x.hppl)}");
            }

        }

        private static void Exercise2()
        {
            XmlSerializer ser = new(typeof(List<Car>), new XmlRootAttribute("cars"));

            XmlWriter writer = XmlWriter.Create("CarsCollection.xml");
            ser.Serialize(writer, myCars);
            Console.WriteLine("Result saved in CarsCollection.xml");

            writer.Close();

            XmlReader reader = XmlReader.Create("CarsCollection.xml");

            foreach (var car in (List<Car>)ser.Deserialize(reader))
            {
                Console.WriteLine($"{car.model} {car.engine.model} {car.year}");
            }

            reader.Close();
        }

        private static void Exercise3()
        {
            XDocument rootNode = XDocument.Load("CarsCollection.xml");
            double avgHP = (double)rootNode.XPathEvaluate("sum(cars/car/engine[@model != 'TDI']/horsePower) div count(cars/car/engine[@model != 'TDI'])");
            Console.WriteLine("Avg HP: " + avgHP);

            IEnumerable<XElement> models = rootNode.XPathSelectElements("cars/car[not(model = following-sibling::car/model)]/model");
            foreach (var model in models)
            {
                Console.WriteLine(model.Value);
            }

        }

        private static void Exercise4()
        {

            IEnumerable<XElement> nodes = from car in myCars
                                          select new XElement("car",
                                              new XElement("model", car.model),
                                              new XElement("engine",
                                                  new XAttribute("model", car.engine.model),
                                                  new XElement("displacement", car.engine.displacement),
                                                  new XElement("horsePower", car.engine.horsePower)
                                              ),
                                              new XElement("year", car.year));

            XElement rootNode = new("cars", nodes);
            rootNode.Save("CarsFromLinq.xml");
            Console.WriteLine("Result saved in CarsFromLinq.xml");

        }
        private static void Exercise5()
        {
            XDocument doc = new(
                new XElement("html",
                    new XElement("head",
                        new XElement("title", "Cars Collection"),
                        new XElement("style", "table, th, td {border: 1px solid;}")
                    ),
                    new XElement("body",
                        new XElement("table",
                            new XElement("tr",
                                new XElement("th", "Model"),
                                new XElement("th", "Engine"),
                                new XElement("th", "Displacement"),
                                new XElement("th", "HorsePower"),
                                new XElement("th", "Year")
                            ),
                            from car in myCars
                            select new XElement("tr",
                                new XElement("td", car.model),
                                new XElement("td", car.engine.model),
                                new XElement("td", car.engine.displacement),
                                new XElement("td", car.engine.horsePower),
                                new XElement("td", car.year)
                            )
                        )
                    )
                )
            );

            doc.Save("CarsCollection.html");
            Console.WriteLine("Result saved in CarsCollection.html");
        }
        private static void Exercise6()
        {
            XDocument doc = XDocument.Load("CarsCollection.xml");

            foreach (XElement element in doc.Descendants("horsePower"))
            {
                element.Name = "hp";
            }

            foreach (XElement car in doc.Descendants("car"))
            {
                car.Element("model").Add(new XAttribute("year", car.Element("year").Value));

                car.Element("year").Remove();
            }

            doc.Save("CarsCollection2.xml");
            Console.WriteLine("Result saved in CarsCollection2.xml");

        }


    }
}