using System.Xml.Serialization;

namespace Lab3
{
    [XmlType(TypeName = "car")]
    public class Car
    {
        public string model;
        public Engine engine;
        public int year;

        public Car() { }

        public Car(string model, Engine engine, int year)
        {
            this.model = model;
            this.engine = engine;
            this.year = year;
        }
    }
}
