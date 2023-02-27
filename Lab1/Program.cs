using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;

namespace Lab1
{
    static class Program
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

        static DateTime GetOldestDate(this DirectoryInfo directory)
        {
            DateTime oldestDate = DateTime.Now;

            foreach (FileInfo file in directory.GetFiles())
            {
                if (file.CreationTime < oldestDate)
                {
                    oldestDate = file.CreationTime;
                }
            }

            foreach (DirectoryInfo dir in directory.GetDirectories())
            {
                DateTime time = GetOldestDate(dir);
                if (time < oldestDate)
                {
                    oldestDate = time;
                }
            }

            return oldestDate;
        }

        static string GetRahs(this FileSystemInfo fsi)
        {
            string rahs = "";

            FileAttributes attributes = fsi.Attributes;

            if ((FileAttributes.ReadOnly & attributes) == FileAttributes.ReadOnly)
            {
                rahs += 'r';
            }
            else
            {
                rahs += '-';
            }
            if ((FileAttributes.Archive & attributes) == FileAttributes.Archive)
            {
                rahs += 'a';
            }
            else
            {
                rahs += '-';
            }
            if ((FileAttributes.Hidden & attributes) == FileAttributes.Hidden)
            {
                rahs += 'h';
            }
            else
            {
                rahs += '-';
            }
            if ((FileAttributes.System & attributes) == FileAttributes.System)
            {
                rahs += 's';
            }
            else
            {
                rahs += '-';
            }

            return rahs;
        }

        static void CreateCollection(DirectoryInfo path)
        {
            SortedDictionary<string, int> collection = new SortedDictionary<string, int>(new Comparer());

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

            SortedDictionary<string, int> collection = null;

            FileStream fs = new FileStream("DataFile.dat", FileMode.Open);
            try
            {
                BinaryFormatter formatter = new BinaryFormatter();

                collection = (SortedDictionary<string, int>)formatter.Deserialize(fs);
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
