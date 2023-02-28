package gt;

import javafx.fxml.*;
import java.util.Date;
import java.util.ArrayList;
import java.net.URL; 
import java.time.LocalDate;
import java.io.*;
import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.*;
import javafx.scene.control.*;
import javafx.scene.chart.*;
import javafx.scene.layout.*;
import javafx.stage.*;
import javafx.collections.FXCollections;

public class main extends Application  {
	private static ArrayList<Test> tests;
	private static ArrayList<String> classList;
	private static MainWindowFXMLController controller;

	public static void addTest (Test test) { 
		int index = -1;
		for (Test t: tests){
			index++;
			if(t.getId() == test.getId()){
				tests.set(index, test);
				controller.updateTestList(); 
				return;
			}
		}
		tests.add(test);
		controller.updateTestList(); 
	}
	public static void addSubject (String subject) { classList.add(subject); }
	public static ArrayList<Test> getTests () { return tests; }
	public static ArrayList<String> getSubjects () { return classList; }
	public static void removeTest(Test test) { tests.remove(test); }
	public static void removeSubject(String subject) { 
		classList.remove(subject);
		for (int i=0; i<tests.size(); i++){
			if (tests.get(i).getSubject().equals(subject)){
				tests.remove(i);
				i--;
			}
		}
	}

	@Override
	public void start(Stage primaryStage) {
		//Load serialized test data
		try {
			FileInputStream fis = new FileInputStream("tests.ser");
			ObjectInputStream ois = new ObjectInputStream(fis);
			tests = (ArrayList<Test>) ois.readObject();
			ois.close();
			fis.close();
		} catch (IOException i) {
			i.printStackTrace();
			return;
		} catch (ClassNotFoundException c) {
			c.printStackTrace();
			return;
		}

		//Load serialized subject data
		try {
			FileInputStream fis = new FileInputStream("subjects.ser");
			ObjectInputStream ois = new ObjectInputStream(fis);
			classList = (ArrayList<String>) ois.readObject();
			ois.close();
			fis.close();
		} catch (IOException i) {
			i.printStackTrace();
			return;
		} catch (ClassNotFoundException c) {
			c.printStackTrace();
			return;
		}
		
		Test.setId(tests.stream().max((t1, t2) -> t1.getId() - t2.getId()).get().getId() + 1);
		/*	
		tests = new ArrayList<Test>();
		classList = new ArrayList<String>();
		classList.add("Math");
		//Add Test
		//	public Test(String name, String reflection, String subject, LocalDate date, int score, int total) {
		tests.add(new Test("Test 1", "I did good", "Math", LocalDate.of(2017, 10, 10), 100, 100));
		tests.add(new Test("Test 2", "I did bad", "Math", LocalDate.of(2017, 10, 10), 50, 100));
		tests.add(new Test("Test 3", "I did good", "Math", LocalDate.of(2017, 10, 10), 100, 100));
		tests.add(new Test("Test 4", "I did bad", "Math", LocalDate.of(2017, 10, 10), 50, 100));
		tests.add(new Test("Test 5", "I did good", "Math", LocalDate.of(2017, 10, 10), 100, 100));
		tests.add(new Test("Test 6", "I did bad", "Math", LocalDate.of(2017, 10, 10), 50, 100));
		*/
		try
		{
			controller = new MainWindowFXMLController();
			FXMLLoader mainLoader = new FXMLLoader();
			mainLoader.setLocation(getClass().getResource("main.fxml"));
			mainLoader.setController(controller);
			Stage mainStage = new Stage();
			mainStage.setTitle("Grade Tracker");
			mainStage.setScene(new Scene(mainLoader.load()));
			mainStage.show();
		}
		catch (IOException e) { e.printStackTrace(); }
	}
	@Override
	public void stop() {
		//Serialize test data
		try {
			FileOutputStream fos = new FileOutputStream("tests.ser");
			ObjectOutputStream oos = new ObjectOutputStream(fos);
			oos.writeObject(tests);
			oos.close();
			fos.close();
		} catch (IOException i) {
			i.printStackTrace();
		}
		
		//Serialize subject data
		try {
			FileOutputStream fos = new FileOutputStream("subjects.ser");
			ObjectOutputStream oos = new ObjectOutputStream(fos);
			oos.writeObject(classList);
			oos.close();
			fos.close();
		} catch (IOException i) {
			i.printStackTrace();
		}
	}
	public static void main(String[] args) {
		launch(args);
	}
}

