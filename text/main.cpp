//
//  main.cpp
//  problem
//
//  Created by Eun Ho Lee on 01/01/2020.
//  Copyright © 2020 Eun Ho Lee. All rights reserved.
//

#include "main.hpp"

#include <iostream>
using namespace std;

class Book
{
private:
    int current_page_;
    void set_percent();
public:
    Book(const string& title, int total_page);
    string title_;
    int total_page_;
    double percent_;
    void Move(int page);
    void Open();
    void Read();
    const Book& ThickerBook(const Book&);
};

int main(void)
{
    Book web_book("HTML과 CSS", 350);
    Book html_book("HTML 레퍼런스", 200);
    
    cout << web_book.ThickerBook(html_book).title_;    // 더 두꺼운 책의 이름을 출력함.
    return 0;
}

Book::Book(const string& title, int total_page)
{
    title_ = title;
    total_page_ = total_page;
    current_page_ = 0;
    set_percent();
}

void Book::set_percent()
{
    percent_ = (double) current_page_ / total_page_ * 100;
}

const Book& Book::ThickerBook(const Book& comp_book)
{
    if (comp_book.total_page_ > this->total_page_)
    {
        return comp_book;
    }
    else
    {
        return *this;
    }
}
