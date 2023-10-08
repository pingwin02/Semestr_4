using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;

namespace Lab1
{
    public static class Program
    {
        static void Main(string[] args)
        {
            string path = args[0];
            PrintRecursiveFiles(path, 0);
            Console.WriteLine($"\nNajstarszy plik: {new DirectoryInfo(path).GetOldestDate()}\n");
            CreateCollection(new DirectoryInfo(path));
            Deserialize();

        }

        static void PrintRecursiveFiles(string path, int depth)
        {
            string[] files = Directory.GetFiles(path);
            string[] dirs = Directory.GetDirectories(path);

            Console.WriteLine($"{path.Split("\\").Last()} ({files.Length + dirs.Length}) {new FileInfo(path).GetRahs()}");

            foreach (string dir in dirs)
            {
                for (int i = 0; i <= depth; i++)
                {
                    Console.Write("\t");
                }
                PrintRecursiveFiles(dir, depth + 1);
            }

            foreach (string file in files)
            {
                for (int i = 0; i <= depth; i++)
                {
                    Console.Write("\t");
                }
                Console.WriteLine($"{file.Split("\\").Last()} {new FileInfo(file).Length} bajtow  {new FileInfo(file).GetRahs()}");
            }

        }

        static void CreateCollection(DirectoryInfo path)
        {
            SortedList<string, int> collection = new SortedList<string, int>(new Comparer());

            foreach (DirectoryInfo dir in path.GetDirectories())
            {
                collection.Add(dir.Name, dir.GetFiles().Length + dir.GetDirectories().Length);
            }

            foreach (FileInfo file in path.GetFiles())
            {
                collection.Add(file.Name, (int)file.Length);
            }

            FileStream fs = new FileStream("DataFile.dat", FileMode.Create);
            BinaryFormatter formatter = new BinaryFormatter();
            try
            {
                formatter.Serialize(fs, collection);
            }
            catch (SerializationException e)
            {
                Console.WriteLine("Failed to serialize. Reason: " + e.Message);
                throw;
            }
            finally
            {
                fs.Close();
            }

        }

        static void Deserialize()
        {

            SortedList<string, int> collection = null;

            FileStream fs = new FileStream("DataFile.dat", FileMode.Open);
            try
            {
                BinaryFormatter formatter = new BinaryFormatter();

                collection = (SortedList<string, int>)formatter.Deserialize(fs);
            }
            catch (SerializationException e)
            {
                Console.WriteLine("Failed to deserialize. Reason: " + e.Message);
                throw;
            }
            finally
            {
                fs.Close();
            }

            foreach (var file in collection)
            {
                Console.WriteLine($"{file.Key} -> {file.Value}");
            }
        }

    }
}
