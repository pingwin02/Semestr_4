using System.Xml.Serialization;

namespace Lab3
{
    [XmlType(TypeName = "car")]
    public class Car
    {
        public string model;
        [XmlElement(ElementName = "engine")]
        public Engine motor;
        public int year;

        public Car() { }

        public Car(string model, Engine motor, int year)
        {
            this.model = model;
            this.motor = motor;
            this.year = year;
        }
    }
}
