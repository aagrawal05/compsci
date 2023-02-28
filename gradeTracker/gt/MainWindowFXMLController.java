package gt;

import java.time.LocalDate;
import javafx.event.ActionEvent;
import javafx.fxml.*;
import javafx.scene.text.Text;
import javafx.scene.control.*;
import javafx.scene.*;
import javafx.stage.*;
import javafx.scene.chart.*;
import javafx.collections.FXCollections;
import java.net.URL; 
import java.io.IOException;
import java.util.ResourceBundle;
import java.util.ArrayList;
import javafx.beans.value.*;
import javafx.util.StringConverter;
import javafx.event.*;
import javafx.scene.input.MouseEvent;
import javafx.scene.control.Alert.AlertType;
import java.util.Optional;

public class MainWindowFXMLController implements Initializable {
	
	private ArrayList<String> currentlySelectedSubjects = new ArrayList<String>();
	private ArrayList<Test> filteredTests = new ArrayList<Test>();
	private int dateToNumber (LocalDate date) { return date.getDayOfMonth() + date.getMonthValue() * 100 + date.getYear() * 10000; }
	private String numberToDate (int number) { return String.format("%02d", number % 100) + "/" + String.format("%02d", (number / 100) % 100) + "/" + (number / 10000); }

	public void updateTestList() {
		chart.getData().clear();
		filteredTests = new ArrayList<>(main.getTests());
		if (currentlySelectedSubjects.size() > 0) filteredTests.removeIf(test -> !currentlySelectedSubjects.contains(test.getSubject()));
		testList.setItems(FXCollections.observableArrayList(filteredTests));
		ArrayList<XYChart.Series<Number, Number>> series = new ArrayList<XYChart.Series<Number, Number>>();
		for (String s: main.getSubjects()) series.add(new XYChart.Series<Number, Number>());
		for (Test t: main.getTests()) {
			int index = main.getSubjects().indexOf(t.getSubject());
			series.get(index).getData().add(new XYChart.Data<Number, Number>(dateToNumber(t.getDate()), t.percent()));
		}
		for (int i = 0; i < main.getSubjects().size(); i++) {
			if (currentlySelectedSubjects.contains(main.getSubjects().get(i)) || currentlySelectedSubjects.size() == 0) {
				series.get(i).setName(main.getSubjects().get(i));
				chart.getData().add(series.get(i));
			}
		}
		if (main.getTests().size() > 0) {
			int minDate = dateToNumber(main.getTests().stream().min((t1, t2) -> dateToNumber(t1.getDate()) - dateToNumber(t2.getDate())).get().getDate());
			int maxDate = dateToNumber(main.getTests().stream().max((t1, t2) -> dateToNumber(t1.getDate()) - dateToNumber(t2.getDate())).get().getDate());
			double distance = maxDate - minDate;
			distance = Double.max(distance/10.0, 1.0);	
			dateAxis.setLowerBound(minDate - distance);
			dateAxis.setUpperBound(maxDate + distance);
			dateAxis.setTickUnit((int) (distance/5.0));
		} else {
			dateAxis.setLowerBound(0);
			dateAxis.setUpperBound(0);
		}
	}

	@FXML
	private MenuButton subjectSelector;
	
	@FXML
	private NumberAxis dateAxis;

	@FXML
	private NumberAxis scoreAxis;

	@FXML
	private LineChart<Number, Number> chart;

	@FXML
	private ListView<Test> testList;

	@FXML
	private TextField subjectField;

	@FXML
	private Text reflectionText;

	@FXML
	protected void handleNewTest(ActionEvent event) {
		try {
			FXMLLoader loader = new FXMLLoader();
			loader.setLocation(getClass().getResource("/gt/TestWindow.fxml"));
			loader.setController(new TestWindowFXMLController());
			Stage stage = new Stage();
			stage.setScene(new Scene(loader.load()));
			stage.show();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	@FXML
	protected void handleNewSubject(ActionEvent event) {
		System.out.println("New Subject Added: " + subjectField.getText());
		if (!subjectField.getText().equals("")) {
			if (main.getSubjects().contains(subjectField.getText())) {
				Alert a = new Alert(AlertType.WARNING, "Subject already exists");
				a.showAndWait();
				return;
			} 
			main.addSubject(subjectField.getText());
			CheckMenuItem newItem = new CheckMenuItem(subjectField.getText());
			newItem.setOnAction(new EventHandler<ActionEvent>() {
				@Override
				public void handle(ActionEvent event) {
					if (!currentlySelectedSubjects.contains(newItem.getText())) currentlySelectedSubjects.add(newItem.getText());
					else currentlySelectedSubjects.remove(newItem.getText());
					updateTestList();
				}
			});
			subjectSelector.getItems().add(newItem);
			updateTestList();
			subjectField.setText("");
		}
	}
	
	@FXML
	protected void handleRemoveSubject(ActionEvent event) {
		if (!main.getSubjects().contains(subjectField.getText())) {
			Alert a = new Alert(AlertType.WARNING, "Subject does not exist");
			a.showAndWait();
			return;
		}
		System.out.println("Subject Removed: " + subjectField.getText());
		if (main.getTests().stream().anyMatch(test -> test.getSubject().equals(subjectField.getText()))) {
			Alert a = new Alert(AlertType.CONFIRMATION, "Are you sure you want to delete this subject? All tests associated with this subject will be deleted.");
			Optional<ButtonType> result = a.showAndWait();
			if (result.get() == ButtonType.OK) { main.getTests().removeIf(test -> test.getSubject().equals(subjectField.getText())); return; }
		}
		main.removeSubject(subjectField.getText());
		subjectSelector.getItems().removeIf(item -> item.getText().equals(subjectField.getText()));
		if (currentlySelectedSubjects.contains(subjectField.getText())) currentlySelectedSubjects.remove(subjectField.getText());
		
		updateTestList();
		subjectField.setText("");
	}


	@FXML
	protected void handleEditTest(ActionEvent event) {
		try {
			FXMLLoader loader = new FXMLLoader();
			loader.setLocation(getClass().getResource("/gt/EditWindow.fxml"));
			loader.setController(new EditWindowFXMLController(testList.getSelectionModel().getSelectedItem()));
			Stage stage = new Stage();
			stage.setScene(new Scene(loader.load()));
			stage.show();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@FXML 
	protected void handleRemoveTest(ActionEvent event) {
		main.removeTest(testList.getSelectionModel().getSelectedItem());
		updateTestList();
	}

	@Override
	public void initialize(URL location, ResourceBundle resources) {
		assert subjectSelector != null : "fx:id=\"subjectSelector\" was not injected: check your FXML file 'main.fxml'.";
		assert chart != null : "fx:id=\"chart\" was not injected: check your FXML file 'main.fxml'.";
		assert testList != null : "fx:id=\"testList\" was not injected: check your FXML file 'main.fxml'.";
		assert subjectField != null : "fx:id=\"subjectField\" was not injected: check your FXML file 'main.fxml'.";
		assert reflectionText != null : "fx:id=\"reflectionText\" was not injected: check your FXML file 'main.fxml'.";

		//subjectSelector.setItems(FXCollections.observableArrayList(main.getSubjects()));
		for (String s: main.getSubjects()) {
			CheckMenuItem item = new CheckMenuItem(s);
			item.setOnAction(new EventHandler<ActionEvent>() {
				@Override
				public void handle(ActionEvent event) {
					if (!currentlySelectedSubjects.contains(item.getText())) currentlySelectedSubjects.add(item.getText());
					else currentlySelectedSubjects.remove(item.getText());
					updateTestList();
				}
			});
			subjectSelector.getItems().add(item);
		}
		testList.getSelectionModel().selectedItemProperty().addListener(new ChangeListener<Test>() {
			@Override
			public void changed(ObservableValue<? extends Test> observable, Test oldValue, Test newValue) {
				if (newValue != null) reflectionText.setText("Reflection: " + newValue.getReflection());
				else reflectionText.setText("Reflection: ");
			}
		});

		testList.setOnMouseClicked(new EventHandler<MouseEvent>() {
			@Override
			public void handle(MouseEvent event) {
				if (event.getClickCount() == 2) {
					try {
						FXMLLoader loader = new FXMLLoader();
						loader.setLocation(getClass().getResource("/gt/EditWindow.fxml"));
						loader.setController(new EditWindowFXMLController(testList.getSelectionModel().getSelectedItem()));
						Stage stage = new Stage();
						stage.setScene(new Scene(loader.load()));
						stage.show();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			}
		});

		//Setup Up Chart
		ArrayList<XYChart.Series<Number, Number>> series = new ArrayList<XYChart.Series<Number, Number>>();
		for (String s: main.getSubjects()) series.add(new XYChart.Series<Number, Number>());
		for (Test t: main.getTests()) {
			int index = main.getSubjects().indexOf(t.getSubject());
			series.get(index).getData().add(new XYChart.Data<Number, Number>(dateToNumber(t.getDate()), t.percent()));
		}
		for (int i = 0; i < main.getSubjects().size(); i++) {
			if (currentlySelectedSubjects.contains(main.getSubjects().get(i)) || currentlySelectedSubjects.size() == 0) {
				series.get(i).setName(main.getSubjects().get(i));
				chart.getData().add(series.get(i));
			}
		}

		dateAxis.setAutoRanging(false);
		if (main.getTests().size() > 0) {
			int minDate = dateToNumber(main.getTests().stream().min((t1, t2) -> dateToNumber(t1.getDate()) - dateToNumber(t2.getDate())).get().getDate());
			int maxDate = dateToNumber(main.getTests().stream().max((t1, t2) -> dateToNumber(t1.getDate()) - dateToNumber(t2.getDate())).get().getDate());
			double distance = maxDate - minDate;
			distance = Double.max(distance/10.0, 1.0);	
			dateAxis.setLowerBound(minDate - distance);
			dateAxis.setUpperBound(maxDate + distance);
			dateAxis.setTickUnit((int) (distance/10.0));
		} else {
			dateAxis.setLowerBound(0);
			dateAxis.setUpperBound(0);
		}
    		dateAxis.setTickLabelFormatter(new StringConverter<Number>() {
			@Override
			public String toString(Number object) { return numberToDate(object.intValue()); }

			@Override
			public Number fromString(String string) { return null; }
    		});

		updateTestList();
	}
}
