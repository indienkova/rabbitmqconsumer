using System;
using System.Collections.Generic;
using System.Text;

namespace RabbitMQProducer
{
    public class BookModel
    {
        public string Id { get; set; }

        public string Author { get; set; }

        public string Title { get; set; }

        public int PagesCount { get; set; }
    }
}
