import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import java.io.File
import java.io.FileOutputStream
import java.net.URL
import java.nio.channels.Channels

const val year = 2018

fun download(url: String, name: String) {
    val path = "download/$year/$name"
    val file = File(path)
    if (file.exists()) {
        println("already downloaded!! $url")
        return
    }

    println("downloading $url")

    val webSite = URL(url)
    try {
        val readableByteChannel = Channels.newChannel(webSite.openStream())
        file.parentFile.mkdirs()
        val fileOutputStream = FileOutputStream(path)
        fileOutputStream.channel.transferFrom(readableByteChannel, 0, Long.MAX_VALUE)
    } catch(e: Exception) {
        e.printStackTrace()
    }
}

fun main() {
    val doc: Document = Jsoup.connect("https://www.piano-e-competition.com/midi_$year.asp").get()
    val href = doc.getElementsByTag("a")

    for (element in href) {
        var link: String = element.attr("href") ?: continue
        link = link.replace(" ", "%20")
        val split = link.split("/")

        if (split.size <= 1) continue

        if (split[1].lowercase() == "midifiles" && link.split(".").last().lowercase() == "mid") {
            download("https://www.piano-e-competition.com/$link", split.last())
        }
    }
}