package gt;
import java.time.LocalDate;
import java.io.Serializable;

public class Test implements Serializable
{	
	private static final long serialVersionUID = 6529685098267757690L;

	private static int count = 0;
	private String name;
	private String subject;
	private String reflection;
	private LocalDate date;
	private int score;
	private int total;
	private int id;
	
	public static void setId(int id) { Test.count = id; }


	public Test(String name, String reflection, String subject, LocalDate date, int score, int total) {
		this.name = name;
		this.subject = subject;
		this.date = date;
		this.score = score;
		this.total = total;
		this.reflection = reflection;
		this.id = Test.count++;
	}

	public Test(String name, String reflection, String subject, LocalDate date, int score, int total, int id) {
		this.name = name;
		this.subject = subject;
		this.date = date;
		this.score = score;
		this.total = total;
		this.reflection = reflection;
		this.id = id;
	}
	
	//Getters
	public String getReflection() { return reflection; }
	public String getName() { return name; } 
	public String getSubject() { return subject; }
	public LocalDate getDate() { return date; }
	public int getScore() { return score; }
	public int getTotal() { return total; }
	public int getId() { return id; }

	//Setters
	public void setReflection(String reflection) { this.reflection = reflection; }
	public void setName(String name) { this.name = name; }
	public void setSubject(String subject) { this.subject = subject; }
	public void setDate(LocalDate date) { this.date = date; }
	public void setScore(int score) { this.score = score; }
	public void setTotal(int total) { this.total = total; }

	@Override
	public String toString() { return subject + ": " + name + " - " + date + ", " + score + "/" + total + ", " + ((int)(this.percent()*100))/100.0 + "%"; }

	public double percent() { return 100 * (double)score / total; }


}
