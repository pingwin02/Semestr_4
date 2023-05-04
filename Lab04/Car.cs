using System.Xml.Serialization;

namespace Lab4
{
    [XmlType(TypeName = "car")]
    public class Car
    {
        public string Model { get; set; }
        [XmlElement(ElementName = "engine")]
        public Engine Motor { get; set; }
        public int Year { get; set; }

        public Car() { }

        public Car(string model, Engine motor, int year)
        {
            this.Model = model;
            this.Motor = motor;
            this.Year = year;
        }
    }
}
