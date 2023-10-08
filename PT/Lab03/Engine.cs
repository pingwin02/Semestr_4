using System.Xml.Serialization;

namespace Lab3
{
    public class Engine
    {
        public double displacement;
        public double horsePower;
        [XmlAttribute(AttributeName = "model")]
        public string model;

        public Engine() { }
        public Engine(double displacement, double horsePower, string model)
        {
            this.displacement = displacement;
            this.horsePower = horsePower;
            this.model = model;
        }

    }
}
